import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

BASE_URL = "http://server:8080/api"

st.set_page_config(page_title="Crypto Prediction Dashboard", layout="wide")

# Funções para se conectar ao backend
def get_btc_data():
  response = requests.get(f"{BASE_URL}/coin/btc")
  return response.json()

def get_eth_data():
  response = requests.get(f"{BASE_URL}/coin/eth")
  return response.json()

def get_predictions():
  response = requests.get(f"{BASE_URL}/model/predict")
  return response.json()

def retrain_model():
  response = requests.post(f"{BASE_URL}/model/retrain_model")
  
  if response.status_code == 200:
    return response.json()
  else:
    st.error(f"Erro: {response.status_code} - {response.text}")
    return None

def insert_coin_data():
  response = requests.post(f"{BASE_URL}/coin/insert")
  
  if response.status_code == 200:
    return response.json()
  else:
    st.error(f"Erro ao inserir dados: {response.status_code} - {response.text}")
    return None

# Título e descrição do app
st.title("Crypto Prediction Dashboard")
st.write("O Dashboard oferece uma visão clara do desempenho histórico e previsões de preços de Bitcoin e Ethereum, ajudando investidores a tomar decisões informadas no mercado de criptomoedas.")

# Filtro para selecionar o período diretamente na página
st.header("Filtro de Período")
period = st.selectbox(
  "Escolha o período:",
  ["1 semana", "1 mês", "1 ano", "4 anos"],
)

# Mapeia as opções para o número de dias
period_mapping = {
  "1 semana": 7,
  "1 mês": 30,
  "1 ano": 365,
  "4 anos": 1460
}

# Obtém os dados para BTC e ETH
btc_data = get_btc_data()
eth_data = get_eth_data()

# Verifica se os dados estão vazios
if not btc_data or not eth_data:
  st.warning("Os dados de BTC ou ETH estão vazios. Por favor, insira os dados.")
  
  # Botão para inserir dados
  if st.button("Inserir Dados"):
    with st.spinner("Inserindo dados para BTC e ETH..."):
      response = insert_coin_data()
      if response is not None and response.get('message') == "Data inserted for 'BTC-USD' and 'ETH-USD'":
        st.success("Dados inseridos com sucesso! Recarregue a página para ver os dados.")
      else:
        st.error("Erro ao inserir os dados.")
else:
  predictions = get_predictions()
  # Extrai as previsões
  btc_predict = predictions['btc_prediction']
  eth_predict = predictions['eth_prediction']

  # Converte os dados em DataFrames
  btc_df = pd.DataFrame(btc_data)
  eth_df = pd.DataFrame(eth_data)

  # Filtra os DataFrames com base no período
  if not btc_df.empty and not eth_df.empty:
    # Converter a coluna 'date' para datetime
    btc_df['date'] = pd.to_datetime(btc_df['date'])
    eth_df['date'] = pd.to_datetime(eth_df['date'])

    # Define a data de corte para o filtro
    cut_date = datetime.now() - timedelta(days=period_mapping[period])

    # Aplica o filtro nos DataFrames
    btc_df_filtered = btc_df[btc_df['date'] >= cut_date]
    eth_df_filtered = eth_df[eth_df['date'] >= cut_date]

    # Exibe os gráficos e métricas na mesma página
    # Layout de duas colunas mais largas
    col1, col2 = st.columns([1, 1])  # As colunas ocupam 50% da largura cada

    # Coluna 1 - BTC
    with col1:
      st.subheader("BTC-USD")

      btc_current_price = btc_df_filtered['close'].iloc[-1]
      st.metric(label="Preço Atual do BTC", value=f"${btc_current_price:,.2f}")
      st.metric(label="Previsão do BTC para amanhã", value=f"${btc_predict:,.2f}", delta=f"${btc_predict - btc_df_filtered['close'].iloc[-1]:,.2f}")

      # Previsão de preço do BTC
      btc_predict_df = pd.DataFrame({
        'date': [btc_df_filtered['date'].max() + pd.Timedelta(days=1)],
        'close': [btc_predict]
      })
      btc_df_combined = pd.concat([btc_df_filtered, btc_predict_df], ignore_index=True)

      # Gráfico de linha com previsão
      st.line_chart(btc_df_combined.set_index('date')['close'], use_container_width=True)

      # Mostrar DataFrame filtrado
      st.subheader("Dados BTC Filtrados")
      st.dataframe(btc_df_filtered)

    # Coluna 2 - ETH
    with col2:
      st.subheader("ETH-USD")

      # Caixa de destaque para a previsão do ETH
      eth_current_price = eth_df_filtered['close'].iloc[-1]
      st.metric(label="Preço Atual do ETH", value=f"${eth_current_price:,.2f}")
      st.metric(label="Previsão do ETH para amanhã", value=f"${eth_predict:,.2f}", delta=f"${eth_predict - eth_df_filtered['close'].iloc[-1]:,.2f}")

      # Previsão de preço do ETH
      eth_predict_df = pd.DataFrame({
        'date': [eth_df_filtered['date'].max() + pd.Timedelta(days=1)],
        'close': [eth_predict]
      })
      eth_df_combined = pd.concat([eth_df_filtered, eth_predict_df], ignore_index=True)

      # Gráfico de linha com previsão
      st.line_chart(eth_df_combined.set_index('date')['close'], use_container_width=True)

      # Mostrar DataFrame filtrado
      st.subheader("Dados ETH Filtrados")
      st.dataframe(eth_df_filtered)

    # Última data registrada
    last_date_btc = btc_df['date'].max()
    last_date_eth = eth_df['date'].max()

    st.header("Última Data Registrada")
    st.write(f"Última data registrada para BTC: {last_date_btc.date()}")
    st.write(f"Última data registrada para ETH: {last_date_eth.date()}")

    # Botão para retreinar o modelo
    if st.button("Retreinar Modelo"):
      with st.spinner("Retreinando o modelo... Isso pode levar alguns minutos."):
        response = retrain_model()
        if response is not None and response.get('message') == 'Model retrained successfully':
          st.success("Modelo retreinado com sucesso!")
        else:
          st.error("Erro ao retreinar o modelo.")
