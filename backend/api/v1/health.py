from fastapi import APIRouter

from backend.schemas.common import HealthResponse

router = APIRouter()


@router.get("/health", response_model=HealthResponse)
def health_check() -> HealthResponse:
    return HealthResponse(
        status="healthy",
        service="InsightPilot AI Backend",
        version="1.0.0",
    )