from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
)

from backend.api.dependencies.authentication import (
    verify_api_key,
)
from backend.config.settings import get_settings
from backend.core.rate_limit import limiter
from backend.schemas.analytics import (
    AthenaQueryRequest,
    AthenaQueryResponse,
)
from backend.services.athena_service import (
    AthenaQueryError,
    AthenaService,
    UnsafeQueryError,
)


router = APIRouter()
settings = get_settings()


@router.post(
    "/query",
    response_model=AthenaQueryResponse,
    summary="Run a read-only Athena query",
    description=(
        "Executes one safe read-only SQL query against "
        "the InsightPilot Glue Data Catalog database."
    ),
    dependencies=[
        Depends(verify_api_key),
    ],
)
@limiter.limit(
    settings.rate_limit_analytics
)
def run_athena_query(
    request: Request,
    payload: AthenaQueryRequest,
) -> AthenaQueryResponse:
    try:
        result = AthenaService().execute_query(
            query=payload.query,
            timeout_seconds=payload.timeout_seconds,
            max_results=payload.max_results,
        )

        return AthenaQueryResponse(**result)

    except UnsafeQueryError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except AthenaQueryError as exc:
        raise HTTPException(
            status_code=(
                status.HTTP_503_SERVICE_UNAVAILABLE
            ),
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=(
                status.HTTP_503_SERVICE_UNAVAILABLE
            ),
            detail=str(exc),
        ) from exc