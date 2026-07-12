from __future__ import annotations

from typing import Any

import pandas as pd

from backend.services.athena_service import AthenaService
from ml.churn.config import (
    FEATURE_COLUMNS,
    ID_COLUMN,
    TARGET_COLUMN,
)


def _extract_rows(result: Any) -> list[dict]:
    """
    Extract rows from either:
    1. A dictionary response
    2. A Pydantic response model
    3. An object with a rows attribute
    """

    if isinstance(result, dict):
        rows = result.get("rows", [])
    elif hasattr(result, "model_dump"):
        rows = result.model_dump().get("rows", [])
    elif hasattr(result, "rows"):
        rows = result.rows
    else:
        raise TypeError(
            "Athena result does not contain readable rows."
        )

    return rows


def load_churn_data() -> pd.DataFrame:
    selected_columns = [
        ID_COLUMN,
        *FEATURE_COLUMNS,
        TARGET_COLUMN,
    ]

    query = (
    "SELECT "
    + ", ".join(selected_columns)
    + " FROM insightpilot_processed_db.customer_features"
)

    service = AthenaService()

    result = service.execute_query(
        query=query,
        timeout_seconds=60,
        max_results=10000,
    )

    rows = _extract_rows(result)

    if not rows:
        raise ValueError(
            "Athena returned no rows from customer_features."
        )

    dataframe = pd.DataFrame(rows)

    expected_columns = set(selected_columns)
    missing_columns = expected_columns - set(dataframe.columns)

    if missing_columns:
        raise ValueError(
            f"Missing columns from Athena result: "
            f"{sorted(missing_columns)}"
        )

    numeric_columns = [
        *FEATURE_COLUMNS,
        TARGET_COLUMN,
    ]

    for column in numeric_columns:
        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="coerce",
        )

    dataframe = dataframe.dropna(
        subset=[TARGET_COLUMN]
    )

    dataframe[TARGET_COLUMN] = (
        dataframe[TARGET_COLUMN]
        .astype(int)
    )

    valid_labels = set(
        dataframe[TARGET_COLUMN].unique()
    )

    if not valid_labels.issubset({0, 1}):
        raise ValueError(
            "churn_label must contain only 0 and 1."
        )

    if len(valid_labels) < 2:
        raise ValueError(
            "Both churn classes 0 and 1 are required."
        )

    return dataframe