from backend.api.v1.endpoints import data_quality
from fastapi import APIRouter

from backend.api.v1.analytics import (
    router as analytics_router,
)
from backend.api.v1.health import (
    router as health_router,
)
from backend.api.v1.storage import (
    router as storage_router,
)

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

api_router.include_router(
    analytics_router,
    prefix="/analytics",
    tags=["Analytics"],
)

api_router.include_router(
    data_quality.router,
    prefix="/data-quality",
    tags=["Data Quality"],
)
