from fastapi import APIRouter

from src.main.routes import coin_routes

router = APIRouter(
  prefix="/api",
)

router.include_router(coin_routes.router)