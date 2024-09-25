from typing import Dict, List
import yfinance as yf
import pandas as pd

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound

from src.models.entities.bitcoin import Bitcoin
from src.utils.logging_config import logger

class BitcoinRepository:
  def __init__(self, session: Session) -> None:
    self.session = session

  def get(self) -> List[Dict]:
    try:
      coins = (
        self.session
        .query(Bitcoin)
        .all()
      )
      
      logger.info("Bitcoin data fetched successfully.")
      return [
        {
          'date': coin.date,
          'open': float(coin.open),
          'high': float(coin.high),
          'low': float(coin.low),
          'close': float(coin.close),
          'adj_close': float(coin.adj_close),
          'volume': coin.volume
        }
        for coin in coins
      ]
      
    except NoResultFound:
      logger.error("No bitcoin found!")
      raise Exception("No bitcoin found!")

    except Exception as exception:
      logger.error(f"An error occurred: {exception}")
      raise exception


  def insert(self) -> None:
    # Baixando dados de 2020 até hoje
    df = yf.download('BTC-USD', start="2020-01-01", interval="1d")

    # Verificando se há dados
    if df.empty:
      print(f"No data fetched for 'BTC-USD'")
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
      existing_record = self.session.query(Bitcoin).filter_by(date=row['date']).first()
      if existing_record:
        print(f"Data for {row['date']} already exists, skipping.")
        continue

      # Criando o registro
      record = Bitcoin(
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
      logger.info("Data inserted for 'BTC-USD'.")
    except IntegrityError:
      self.session.rollback()
      logger.error(f"Failed to insert data for 'BTC-USD': IntegrityError")
    except Exception as e:
      self.session.rollback()
      logger.error(f"Failed to insert data for 'BTC-USD': {e}")
