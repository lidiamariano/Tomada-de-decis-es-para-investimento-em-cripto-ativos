import pandas as pd
import numpy as np
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Dropout, Activation
from keras.losses import mean_absolute_error
from sqlalchemy.orm import Session

from src.models.repositories.model_repository import ModelRepository

class ModelService:
  def __init__(self, session: Session):
    self.model_repository = ModelRepository(session)
  
  def _transform_to_dataframe(self, data):
    if data is None:
      raise ValueError("O argumento 'data' é None.")
      
    data_dict = [{
      'Date': d['date'],
      'open': d['open'],
      'high': d['high'],
      'low': d['low'],
      'close': d['close'],
      'adj_close': d['adj_close'],
      'volume': d['volume']
    } for d in data]
      
    return pd.DataFrame(data_dict)

  def _generate_market_df(self, btc_df, eth_df):
    # Renomeando as colunas de cada DataFrame
    btc_df.columns = ['Date', 'open_btc', 'high_btc', 'low_btc', 'close_btc', 'adj_close_btc', 'volume_btc']
    eth_df.columns = ['Date', 'open_eth', 'high_eth', 'low_eth', 'close_eth', 'adj_close_eth', 'volume_eth']
    
    # Convertendo a coluna 'Date' para o tipo datetime, para evitar o erro de comparação
    btc_df['Date'] = pd.to_datetime(btc_df['Date'])
    eth_df['Date'] = pd.to_datetime(eth_df['Date'])

    # Merge dos dataframes
    market_df = pd.merge(btc_df, eth_df, on='Date')

    # Adicionando nova coluna da diferença entre o preço de abertura e fechamento
    for coin in ['btc', 'eth']:
      market_df[f'{coin}_day_diff'] = (market_df[f'close_{coin}'] - market_df[f'open_{coin}']) / market_df[f'open_{coin}']

    # Filtrando o DataFrame para datas a partir de 2020-01-01
    market_df = market_df[market_df['Date'] >= pd.Timestamp('2020-01-01')]

    return market_df


  def _prepare_data(self, market_df, window_len=10):
    # Processa os dados
    for coins in ['_btc', '_eth']:
      kwargs = {
        'close_off_high' + coins: lambda x: 2 * (x['high' + coins] - x['close' + coins]) / (x['high' + coins] - x['low' + coins]) - 1,
        'volatility' + coins: lambda x: (x['high' + coins] - x['low' + coins]) / (x['open' + coins])
      }
      market_df = market_df.assign(**kwargs)

    model_data = market_df[['Date'] + [metric + coin for coin in ['_btc', '_eth'] for metric in ['close', 'volume', 'close_off_high', 'volatility']]]
    model_data = model_data.sort_values(by='Date')
    model_data = model_data.drop('Date', axis=1)

    # Normaliza os dados
    norm_cols = [metric + coin for coin in ['_btc', '_eth'] for metric in ['close', 'volume']]
    LSTM_training_inputs = []
    for i in range(len(model_data) - window_len):
      temp_set = model_data[i:(i + window_len)].copy()
      for col in norm_cols:
        temp_set.loc[:, col] = temp_set[col] / temp_set[col].iloc[0] - 1
      LSTM_training_inputs.append(temp_set)
    
    LSTM_training_inputs = np.array(LSTM_training_inputs)
    return LSTM_training_inputs

  def _build_model(self, inputs, output_size, neurons, activ_func="linear", 
                   dropout=0.25, loss="mae", optimizer="adam"):
    model = Sequential()
    model.add(LSTM(neurons, input_shape=(inputs.shape[1], inputs.shape[2])))
    model.add(Dropout(dropout))
    model.add(Dense(units=output_size))
    model.add(Activation(activ_func))
    model.compile(loss=loss, optimizer=optimizer)
    return model

  def _train_models(self, LSTM_training_inputs, training_set, window_len=10):
    btc_model = self._build_model(LSTM_training_inputs, output_size=1, neurons=20)
    btc_history = btc_model.fit(
      LSTM_training_inputs,
      (training_set['close_btc'][window_len:].values / training_set['close_btc'][:-window_len].values) - 1,
      epochs=50, batch_size=1, verbose=2, shuffle=True
    )

    eth_model = self._build_model(LSTM_training_inputs, output_size=1, neurons=20)
    eth_history = eth_model.fit(
      LSTM_training_inputs,
      (training_set['close_eth'][window_len:].values / training_set['close_eth'][:-window_len].values) - 1,
      epochs=50, batch_size=1, verbose=2, shuffle=True
    )

    return btc_model, eth_model, btc_history, eth_history


  def run_pipeline(self, btc_data, eth_data):
    btc_df = self._transform_to_dataframe(btc_data)
    eth_df = self._transform_to_dataframe(eth_data)
    
    market_df = self._generate_market_df(btc_df, eth_df)
    
    LSTM_training_inputs = self._prepare_data(market_df)
    
    btc_model, eth_model, btc_history, eth_history = self._train_models(LSTM_training_inputs, market_df)
    
    eth_model.save('models/eth_model.h5')
    btc_model.save('models/btc_model.h5')
        
    return btc_model, eth_model, btc_history, eth_history
  
  def predict(self, btc_data, eth_data, model_path='models/'):
    # Transformar os dados recebidos em DataFrames
    btc_df = self._transform_to_dataframe(btc_data)
    eth_df = self._transform_to_dataframe(eth_data)
    
    # Gerar o DataFrame de mercado com os dados combinados
    market_df = self._generate_market_df(btc_df, eth_df)
    
    # Preparar os dados de entrada para o modelo
    LSTM_training_inputs = self._prepare_data(market_df)
    
    # Carregar os modelos treinados
    btc_model = load_model(f'{model_path}btc_model.h5', custom_objects={'mae': mean_absolute_error})
    eth_model = load_model(f'{model_path}eth_model.h5', custom_objects={'mae': mean_absolute_error})
    
    # Fazer as previsões
    btc_prediction = btc_model.predict(LSTM_training_inputs[-1:])[0][0]
    eth_prediction = eth_model.predict(LSTM_training_inputs[-1:])[0][0]
    
    # Desnormalizar as previsões para voltarem ao valor original
    btc_last_close = market_df['close_btc'].iloc[-1]
    eth_last_close = market_df['close_eth'].iloc[-1]
    
    btc_prediction = (btc_prediction + 1) * btc_last_close
    eth_prediction = (eth_prediction + 1) * eth_last_close
    
    self.model_repository.insert_predict(btc_prediction, eth_prediction)
    
    return {
      'btc_prediction': btc_prediction,
      'eth_prediction': eth_prediction
    }