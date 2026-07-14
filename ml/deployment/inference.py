from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import joblib
import pandas as pd


MODEL_FILENAME = "churn_model.joblib"


def model_fn(model_dir: str) -> dict[str, Any]:
    """
    Load the packaged churn artifact when the SageMaker
    inference container starts.
    """
    model_path = Path(model_dir) / MODEL_FILENAME

    if not model_path.exists():
        raise FileNotFoundError(
            f"Model artifact was not found at {model_path}"
        )

    return joblib.load(model_path)


def input_fn(
    request_body: str,
    request_content_type: str,
) -> dict[str, Any]:
    """
    Convert an incoming JSON request into a Python dictionary.
    """
    if request_content_type != "application/json":
        raise ValueError(
            "Only application/json requests are supported."
        )

    payload = json.loads(request_body)

    if not isinstance(payload, dict):
        raise ValueError(
            "The prediction payload must be a JSON object."
        )

    return payload


def predict_fn(
    input_data: dict[str, Any],
    model_artifact: dict[str, Any],
) -> dict[str, Any]:
    """
    Generate the churn prediction and probability.
    """
    model = model_artifact["model"]
    feature_columns = model_artifact["feature_columns"]

    missing_features = [
        column
        for column in feature_columns
        if column not in input_data
    ]

    if missing_features:
        raise ValueError(
            "Missing required features: "
            + ", ".join(missing_features)
        )

    row = pd.DataFrame([input_data])

    row = row.reindex(
        columns=feature_columns
    )

    for column in feature_columns:
        row[column] = pd.to_numeric(
            row[column],
            errors="raise",
        )

    prediction = int(
        model.predict(row)[0]
    )

    probability = float(
        model.predict_proba(row)[0][1]
    )

    risk_level = (
        "High"
        if probability >= 0.70
        else "Medium"
        if probability >= 0.40
        else "Low"
    )

    return {
        "churn_prediction": prediction,
        "churn_probability": probability,
        "risk_level": risk_level,
    }


def output_fn(
    prediction: dict[str, Any],
    response_content_type: str,
) -> tuple[str, str]:
    """
    Convert prediction output into JSON.
    """
    if response_content_type != "application/json":
        raise ValueError(
            "Only application/json responses are supported."
        )

    return (
        json.dumps(prediction),
        response_content_type,
    )