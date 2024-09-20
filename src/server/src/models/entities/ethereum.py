from sqlalchemy import Column, BigInteger, Date, Numeric
from src.models.settings.base import Base

class Ethereum(Base):
  __tablename__ = 'ethereum'
  
  id = Column(BigInteger, primary_key=True, autoincrement=True)
  date = Column(Date, nullable=False)
  open = Column(Numeric(12, 2), nullable=False)
  high = Column(Numeric(12, 2), nullable=False)
  low = Column(Numeric(12, 2), nullable=False)
  close = Column(Numeric(12, 2), nullable=False)
  adj_close = Column(Numeric(12, 2), nullable=False)
  volume = Column(BigInteger, nullable=False)
  
  def __repr__(self):
    return "<Ethereum(date={}, open={}, high={}, low={}, close={}, adj_close={}, volume={})>".format(
      self.date,
      self.open,
      self.high,
      self.low,
      self.close,
      self.adj_close,
      self.volume
    )