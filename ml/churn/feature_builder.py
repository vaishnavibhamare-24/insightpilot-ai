from __future__ import annotations

import pandas as pd

from ml.churn.config import (
    FEATURE_COLUMNS,
    TARGET_COLUMN,
)


def build_churn_features(
    dataframe: pd.DataFrame,
) -> tuple[pd.DataFrame, pd.Series]:
    model_data = dataframe.copy()

    missing_columns = [
        column
        for column in FEATURE_COLUMNS
        if column not in model_data.columns
    ]

    if missing_columns:
        raise ValueError(
            f"Missing feature columns: {missing_columns}"
        )

    if TARGET_COLUMN not in model_data.columns:
        raise ValueError(
            f"Missing target column: {TARGET_COLUMN}"
        )

    for column in FEATURE_COLUMNS:
        model_data[column] = pd.to_numeric(
            model_data[column],
            errors="coerce",
        )

    model_data[FEATURE_COLUMNS] = (
        model_data[FEATURE_COLUMNS]
        .replace([float("inf"), float("-inf")], pd.NA)
        .fillna(0)
    )

    model_data[TARGET_COLUMN] = pd.to_numeric(
        model_data[TARGET_COLUMN],
        errors="coerce",
    )

    model_data = model_data.dropna(
        subset=[TARGET_COLUMN]
    )

    model_data[TARGET_COLUMN] = (
        model_data[TARGET_COLUMN]
        .astype(int)
    )

    features = model_data[FEATURE_COLUMNS]
    target = model_data[TARGET_COLUMN]

    return features, target