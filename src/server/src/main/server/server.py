from fastapi import APIRouter

from src.main.routes import coin_routes
from src.main.routes import model_routes

router = APIRouter(
  prefix="/api",
)

router.include_router(model_routes.router)
router.include_router(coin_routes.router)