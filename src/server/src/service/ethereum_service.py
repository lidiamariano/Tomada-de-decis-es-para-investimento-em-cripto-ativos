from sqlalchemy.orm import Session
from src.models.repositories.ethereum_repository import EthereumRepository

class EthereumService:
  def __init__(self, session: Session) -> None:
    self.ethereum_repository = EthereumRepository(session)
    
  def insert(self) -> None:
    self.ethereum_repository.insert()