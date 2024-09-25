from sqlalchemy.orm import Session

from src.models.repositories.ethereum_repository import EthereumRepository
from src.models.entities.ethereum import Ethereum

class EthereumService:
  def __init__(self, session: Session) -> None:
    self.ethereum_repository = EthereumRepository(session)
  
  def get(self) -> Ethereum:
    return self.ethereum_repository.get()
  
  def insert(self) -> None:
    self.ethereum_repository.insert()