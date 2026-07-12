from __future__ import annotations

from typing import Any

import joblib
import pandas as pd

from ml.churn.config import MODEL_PATH


class ChurnPredictor:
    def __init__(self) -> None:
        if not MODEL_PATH.exists():
            raise FileNotFoundError(
                "Churn model was not found. "
                "Run python -m ml.churn.train first."
            )

        artifact = joblib.load(MODEL_PATH)

        self.model = artifact["model"]
        self.feature_columns = artifact["feature_columns"]

    def predict(
        self,
        features: dict[str, Any],
    ) -> dict[str, Any]:
        row = pd.DataFrame([features])

        row = row.reindex(
            columns=self.feature_columns,
            fill_value=0,
        )

        for column in self.feature_columns:
            row[column] = pd.to_numeric(
                row[column],
                errors="coerce",
            ).fillna(0)

        prediction = int(
            self.model.predict(row)[0]
        )

        probability = float(
            self.model.predict_proba(row)[0][1]
        )

        if probability >= 0.70:
            risk_level = "High"
        elif probability >= 0.40:
            risk_level = "Medium"
        else:
            risk_level = "Low"

        return {
            "churn_prediction": prediction,
            "churn_probability": round(
                probability,
                6,
            ),
            "risk_level": risk_level,
        }