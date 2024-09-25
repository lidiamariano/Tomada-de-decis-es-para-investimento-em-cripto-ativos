from sqlalchemy import Column, DateTime, Float, Integer
from src.models.settings.base import Base
import datetime

class Predict(Base):
  __tablename__ = 'predict'
  
  id = Column(Integer, primary_key=True, autoincrement=True)
  date = Column(DateTime, nullable=False, default=datetime.datetime.now)
  btc_predict = Column(Float, nullable=False)
  eth_predict = Column(Float, nullable=False)

  def __repr__(self):
    return "<Predict(id={}, date={}, btc_predict={}, eth_predict={})>";format(
      seld.id,
      self.date,
      self.btc_predict,
      self.eth_predict
    )

  