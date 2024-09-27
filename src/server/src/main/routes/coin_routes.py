from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.models.settings.connection import get_db
from src.service.bitcoin_service import BitcoinService
from src.service.ethereum_service import EthereumService
from src.service.model_service import ModelService
from src.utils.logging_config import logger

router = APIRouter(
  prefix="/coin",
  tags=["Coin"]
)

@router.post("/insert")
def insert_coin_data(
  db: Session = Depends(get_db)
):
  logger.info("Inserting data for 'BTC-USD' and 'ETH-USD'...")
  bitcoin_service = BitcoinService(db)
  bitcoin_service.insert()
  
  ethereum_service = EthereumService(db)
  ethereum_service.insert()
  
  logger.info("Data inserted for 'BTC-USD' and 'ETH-USD'.")
  return {"message": "Data inserted for 'BTC-USD' and 'ETH-USD'"}

@router.get("/btc")
def get_btc_data(
  db: Session = Depends(get_db)
):
  logger.info("Getting data for 'BTC-USD'...")
  bitcoin_service = BitcoinService(db)
  
  logger.info("Data for 'BTC-USD' retrieved successfully.")
  return bitcoin_service.get()

@router.get("/eth")
def get_eth_data(
  db: Session = Depends(get_db)
):
  logger.info("Getting data for 'ETH-USD'...")
  ethereum_service = EthereumService(db)
  
  logger.info("Data for 'ETH-USD' retrieved successfully.")
  return ethereum_service.get()

@router.get("/predict")
def predict(
  db: Session = Depends(get_db)
):
  logger.info("Get Predict...")
  model_service = ModelService(db)
  response = model_service.get_predict()
  
  logger.info("Predictions retrieved successfully.")
  return response