from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.models.settings.connection import get_db
from src.service.bitcoin_service import BitcoinService
from src.service.ethereum_service import EthereumService

router = APIRouter(
  prefix="/coin",
  tags=["Coin"]
)

@router.post("/insert")
def insert_coin_data(
  db: Session = Depends(get_db)
):
  bitcoin_service = BitcoinService(db)
  bitcoin_service.insert()
  
  ethereum_service = EthereumService(db)
  ethereum_service.insert()
  
  return {"message": "Data inserted for 'BTC-USD' and 'ETH-USD'"}

@router.get("/btc")
def get_btc_data(
  db: Session = Depends(get_db)
):
  bitcoin_service = BitcoinService(db)
  return bitcoin_service.get()

@router.get("/eth")
def get_eth_data(
  db: Session = Depends(get_db)
):
  ethereum_service = EthereumService(db)
  return ethereum_service.get()