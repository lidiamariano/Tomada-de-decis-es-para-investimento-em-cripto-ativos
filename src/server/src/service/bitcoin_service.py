from sqlalchemy.orm import Session
from src.models.repositories.bitcoin_repository import BitcoinRepository

class BitcoinService:
  def __init__(self, session: Session) -> None:
    self.bitcoin_repository = BitcoinRepository(session)
    
  def insert(self) -> None:
    self.bitcoin_repository.insert()
    