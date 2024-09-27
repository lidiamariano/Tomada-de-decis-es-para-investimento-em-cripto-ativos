from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from src.models.settings.connection import get_db
from src.service.bitcoin_service import BitcoinService
from src.service.ethereum_service import EthereumService
from src.service.model_service import ModelService
from src.utils.logging_config import logger

router = APIRouter(
  prefix="/model",
  tags=["Model"]
)

@router.post("/train_model")
def train_model(
  db: Session = Depends(get_db)
):
  logger.info("Training model...")
  bitcoin_service = BitcoinService(db)
  btc_data = bitcoin_service.get()
  
  ethereum_service = EthereumService(db)
  eth_data = ethereum_service.get()
  
  model_service = ModelService(db)
  model_service.run_pipeline(btc_data=btc_data, eth_data=eth_data)
  
  logger.info("Model trained successfully.")
  return {"message": "Model trained successfully"}

@router.post("/retrain_model")
def retrain_model(
  db: Session = Depends(get_db)
):
  logger.info("Retraining model...")
  bitcoin_service = BitcoinService(db)
  ethereum_service = EthereumService(db)
  
  bitcoin_service.insert()
  ethereum_service.insert()
  
  btc_data = bitcoin_service.get()
  eth_data = ethereum_service.get()
  
  model_service = ModelService(db)
  model_service.run_pipeline(btc_data=btc_data, eth_data=eth_data)
  
  logger.info("Model retrained successfully.")
  return {"message": "Model retrained successfully"}

@router.get("/predict")
def predict(
  db: Session = Depends(get_db)
):
  logger.info("Predicting...")
  bitcoin_service = BitcoinService(db)
  btc_data = bitcoin_service.get()
  
  ethereum_service = EthereumService(db)
  eth_data = ethereum_service.get()
  
  model_service = ModelService(db)
  
  logger.info("Predicted successfully.")
  return model_service.predict(btc_data=btc_data, eth_data=eth_data)

  
  