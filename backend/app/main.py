from fastapi import FastAPI

from backend.api.v1.router import api_router
from backend.config.settings import get_settings


settings = get_settings()


app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description=(
        "InsightPilot AI analytics, machine learning, "
        "enterprise RAG, and multi-agent API."
    ),
)


@app.get(
    "/",
    tags=["Root"],
)
def root() -> dict[str, str]:
    return {
        "message": "InsightPilot AI API is running.",
        "version": settings.app_version,
        "environment": settings.app_env,
    }


app.include_router(
    api_router,
    prefix="/api/v1",
)
