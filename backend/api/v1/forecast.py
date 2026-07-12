from fastapi import (
    APIRouter,
    HTTPException,
    Query,
)

from backend.schemas.predictions import (
    RevenueForecastResponse,
)
from backend.services.revenue_forecast_service import (
    RevenueForecastService,
)

router = APIRouter()


@router.get(
    "/revenue",
    response_model=RevenueForecastResponse,
)
def forecast_revenue(
    months: int = Query(
        default=6,
        ge=1,
        le=12,
    ),
) -> RevenueForecastResponse:
    try:
        result = RevenueForecastService().forecast(
            months=months
        )

        return RevenueForecastResponse(
            **result
        )

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "Unable to generate revenue forecast. "
                f"{type(exc).__name__}"
            ),
        ) from exc