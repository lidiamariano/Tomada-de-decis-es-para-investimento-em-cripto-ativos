from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
import logging

from src.main.server.server import router
from src.utils.init_db import create_tables
from src.utils.logging_config import logger

app = FastAPI(
  debug=True,
  title="Crypto API",
)

@app.on_event("startup")
def on_startup() -> None:
  logger.info("Starting up and creating tables if they do not exist...")
  create_tables()
  logger.info("Tables created or verified successfully.")
    

app.add_middleware(
  CORSMiddleware,
  allow_origins=["*"],
  allow_credentials=True,
  allow_methods=["*"],
  allow_headers=["*"],
)

app.include_router(router)