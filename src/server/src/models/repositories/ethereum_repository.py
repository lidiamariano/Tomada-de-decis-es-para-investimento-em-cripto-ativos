import yfinance as yf
import pandas as pd

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from src.models.entities.ethereum import Ethereum

class EthereumRepository:
  def __init__(self, session: Session) -> None:
    self.session = session

  def insert(self) -> None:
    # Baixando dados de 2020 até hoje
    df = yf.download('ETH-USD', start="2020-01-01", interval="1d")

    # Verificando se há dados
    if df.empty:
      print(f"No data fetched for 'ETH-USD'")
      return

    # Renomeando colunas para se ajustarem ao modelo
    df.reset_index(inplace=True)
    df.rename(columns={
      'Date': 'date',
      'Open': 'open',
      'High': 'high',
      'Low': 'low',
      'Close': 'close',
      'Adj Close': 'adj_close',
      'Volume': 'volume'
    }, inplace=True)

    # Convertendo os dados para o formato necessário
    df['date'] = pd.to_datetime(df['date']).dt.date

    # Verificando e inserindo apenas novos registros
    for _, row in df.iterrows():
      # Verificando se o registro já existe
      existing_record = self.session.query(Ethereum).filter_by(date=row['date']).first()
      if existing_record:
        print(f"Data for {row['date']} already exists, skipping.")
        continue

      # Criando o registro
      record = Ethereum(
          date=row['date'],
          open=row['open'],
          high=row['high'],
          low=row['low'],
          close=row['close'],
          adj_close=row['adj_close'],
          volume=row['volume']
      )
      self.session.add(record)

    try:
      self.session.commit()
      print(f"Data inserted for 'ETH-USD'")
    except IntegrityError:
      self.session.rollback()
      print(f"Failed to insert data for 'ETH-USD': IntegrityError")
    except Exception as e:
      self.session.rollback()
      print(f"Failed to insert data for 'ETH-USD': {e}")
