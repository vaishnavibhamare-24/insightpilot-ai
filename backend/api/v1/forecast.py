from fastapi import Request

from backend.core.rate_limit import limiter
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Query,
)

from backend.api.dependencies.authentication import (
    verify_api_key,
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
    dependencies=[
        Depends(verify_api_key),
    ],
)
@limiter.limit(
    "20/minute"
)
def forecast_revenue(
    request: Request,
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