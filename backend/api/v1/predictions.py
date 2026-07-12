from fastapi import APIRouter, HTTPException

from backend.schemas.predictions import (
    ChurnPredictionRequest,
    ChurnPredictionResponse,
)
from backend.services.churn_prediction_service import (
    ChurnPredictionService,
)

router = APIRouter()


@router.post(
    "/churn",
    response_model=ChurnPredictionResponse,
)
def predict_churn(
    request: ChurnPredictionRequest,
) -> ChurnPredictionResponse:
    try:
        result = ChurnPredictionService().predict(
            request.model_dump()
        )

        return ChurnPredictionResponse(**result)

    except Exception as exc:
        raise HTTPException(
            status_code=503,
            detail=(
                "Unable to generate churn prediction. "
                f"{type(exc).__name__}"
            ),
        ) from exc