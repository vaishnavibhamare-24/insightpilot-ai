from fastapi import APIRouter

from backend.api.v1.analytics import (
    router as analytics_router,
)
from backend.api.v1.chat import (
    router as chat_router,
)
from backend.api.v1.dashboard import (
    router as dashboard_router,
)
from backend.api.v1.forecast import (
    router as forecast_router,
)
from backend.api.v1.health import (
    router as health_router,
)
from backend.api.v1.predictions import (
    router as predictions_router,
)
from backend.api.v1.rag import (
    router as rag_router,
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
    predictions_router,
    prefix="/predictions",
    tags=["Predictions"],
)

api_router.include_router(
    forecast_router,
    prefix="/forecast",
    tags=["Forecasting"],
)

api_router.include_router(
    rag_router,
    prefix="/rag",
    tags=["Enterprise RAG"],
)

api_router.include_router(
    chat_router,
    prefix="/chat",
    tags=["Multi-Agent AI"],
)

api_router.include_router(
    dashboard_router,
    prefix="/dashboard",
    tags=["Dashboard"],
)