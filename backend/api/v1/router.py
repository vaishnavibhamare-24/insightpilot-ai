from fastapi import APIRouter

from backend.api.v1.health import router as health_router
from backend.api.v1.storage import router as storage_router

api_router = APIRouter()

api_router.include_router(
    health_router,
    prefix="/health",
    tags=["Health"],
)

api_router.include_router(
    storage_router,
    prefix="/storage",
    tags=["Storage"],
)