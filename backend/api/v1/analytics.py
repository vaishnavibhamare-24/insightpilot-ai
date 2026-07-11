from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

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


@router.post(
    "/query",
    response_model=AthenaQueryResponse,
    summary="Run a read-only Athena query",
    description=(
        "Executes one safe read-only SQL query against "
        "the InsightPilot Glue Data Catalog database."
    ),
)
def run_athena_query(
    request: AthenaQueryRequest,
) -> AthenaQueryResponse:
    try:
        result = AthenaService().execute_query(
            query=request.query,
            timeout_seconds=request.timeout_seconds,
            max_results=request.max_results,
        )

        return AthenaQueryResponse(**result)

    except UnsafeQueryError as exc:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(exc),
        ) from exc

    except AthenaQueryError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc