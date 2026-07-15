from fastapi import Request

from backend.core.rate_limit import limiter
from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from backend.api.dependencies.authentication import (
    verify_api_key,
)
from backend.schemas.predictions import (
    ChurnPredictionRequest,
    ChurnPredictionResponse,
)
from backend.services.sagemaker_prediction_service import (
    SageMakerPredictionError,
    SageMakerPredictionService,
)


router = APIRouter()


@router.post(
    "/churn",
    response_model=ChurnPredictionResponse,
    summary="Predict customer churn",
    dependencies=[
        Depends(verify_api_key),
    ],
)
@limiter.limit(
    "20/minute"
)
def predict_churn(
    request: Request,
    payload: ChurnPredictionRequest,
) -> ChurnPredictionResponse:
    try:
        result = (
            SageMakerPredictionService()
            .predict_churn(
                payload.model_dump()
            )
        )

        return ChurnPredictionResponse(
            **result
        )

    except SageMakerPredictionError as exc:
        raise HTTPException(
            status_code=(
                status.HTTP_503_SERVICE_UNAVAILABLE
            ),
            detail=str(exc),
        ) from exc