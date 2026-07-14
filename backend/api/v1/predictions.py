from fastapi import (
    APIRouter,
    HTTPException,
    status,
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
)
def predict_churn(
    request: ChurnPredictionRequest,
) -> ChurnPredictionResponse:
    try:
        result = (
            SageMakerPredictionService()
            .predict_churn(
                request.model_dump()
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