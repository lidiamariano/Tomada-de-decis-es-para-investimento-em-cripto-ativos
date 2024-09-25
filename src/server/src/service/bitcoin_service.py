from typing import Dict, List
from sqlalchemy.orm import Session

from src.models.repositories.bitcoin_repository import BitcoinRepository
from src.models.entities.bitcoin import Bitcoin

class BitcoinService:
  def __init__(self, session: Session) -> None:
    self.bitcoin_repository = BitcoinRepository(session)
    
  def get(self) -> List[Dict]:
   return self.bitcoin_repository.get()

  def insert(self) -> None:
    self.bitcoin_repository.insert()
    