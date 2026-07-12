from functools import lru_cache
from typing import Any

from ml.churn.predict import ChurnPredictor


@lru_cache
def get_churn_predictor() -> ChurnPredictor:
    return ChurnPredictor()


class ChurnPredictionService:
    def predict(
        self,
        features: dict[str, Any],
    ) -> dict[str, Any]:
        predictor = get_churn_predictor()

        return predictor.predict(features)