from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import NoResultFound
from datetime import datetime

from src.models.entities.predict import Predict
from src.utils.logging_config import logger

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
      logger.info("Predictions inserted successfully.")
      
    except IntegrityError:
      logger.error("Integrity Error in inserting predictions.")
      self.session.rollback()
      raise Exception("Integrity Error")
      
    except Exception as exception:
      logger.error(f"An error occurred: {exception}")
      self.session.rollback()
      raise exception
    
  def get_predict(self) -> Predict:
    try:
      predict = self.session.query(Predict).order_by(Predict.date.desc()).first()
      
      if predict is None:
        raise NoResultFound("No predictions found.")
      
      return predict
    
    except NoResultFound as exception:
      logger.error(f"No predictions found: {exception}")
      raise exception
      
    except Exception as exception:
      logger.error(f"An error occurred: {exception}")
      raise exception