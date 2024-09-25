from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

from src.models.entities.predict import Predict

class ModelRepository:
  def __init__(self, session: Session):
    self.session = session
    
  def insert_predict(self, btc_predict: float, eth_predict: float) -> None:
    try:
      predict = Predict(
        date=datetime.now(),
        btc_predict=btc_predict,
        eth_predict=eth_predict
      )
      
      self.session.add(predict)
      self.session.commit()
      
    except IntegrityError:
      self.session.rollback()
      raise Exception("Integrity Error")
      
    except Exception as exception:
      self.session.rollback()
      raise exception