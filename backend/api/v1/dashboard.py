from __future__ import annotations

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from backend.api.dependencies.authentication import (
    verify_api_key,
)
from backend.schemas.dashboard import (
    DashboardMetricsResponse,
)
from backend.services.dashboard_service import (
    DashboardService,
)


router = APIRouter()


@router.get(
    "/metrics",
    response_model=DashboardMetricsResponse,
    summary="Get executive dashboard metrics",
    dependencies=[
        Depends(verify_api_key),
    ],
)
def get_dashboard_metrics(
) -> DashboardMetricsResponse:
    try:
        result = DashboardService().get_metrics()

        return DashboardMetricsResponse(
            **result
        )

    except Exception as exc:
        raise HTTPException(
            status_code=(
                status.HTTP_503_SERVICE_UNAVAILABLE
            ),
            detail=(
                "Unable to load dashboard metrics."
            ),
        ) from exc