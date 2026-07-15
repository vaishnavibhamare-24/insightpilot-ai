from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from backend.config.settings import get_settings
from backend.schemas.health import (
    DetailedHealthResponse,
    LivenessResponse,
    ReadinessResponse,
)
from backend.services.health_service import (
    HealthService,
)


router = APIRouter()
settings = get_settings()


@router.get(
    "",
    response_model=DetailedHealthResponse,
)
def health() -> DetailedHealthResponse:
    readiness = HealthService().readiness()

    return DetailedHealthResponse(
        status=readiness["status"],
        service=settings.app_name,
        version=settings.app_version,
        environment=settings.app_env,
        dependencies=readiness["dependencies"],
        metadata={
            "region": settings.aws_region,
        },
    )


@router.get(
    "/live",
    response_model=LivenessResponse,
)
def live() -> LivenessResponse:
    return LivenessResponse(
        status="alive",
        service=settings.app_name,
        version=settings.app_version,
    )


@router.get(
    "/ready",
    response_model=ReadinessResponse,
)
def ready() -> JSONResponse:
    result = HealthService().readiness()

    status_code = (
        200
        if result["status"] == "ready"
        else 503
    )

    return JSONResponse(
        status_code=status_code,
        content=result,
    )