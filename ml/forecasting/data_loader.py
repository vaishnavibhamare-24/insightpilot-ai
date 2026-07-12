from __future__ import annotations

from typing import Any

import pandas as pd

from backend.services.athena_service import AthenaService
from ml.forecasting.config import (
    BASE_FEATURE_COLUMNS,
    DATE_COLUMN,
    TARGET_COLUMN,
)


def _extract_rows(result: Any) -> list[dict]:
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


def load_revenue_data() -> pd.DataFrame:
    selected_columns = [
        DATE_COLUMN,
        TARGET_COLUMN,
        *BASE_FEATURE_COLUMNS,
    ]

    query = """
        SELECT
            revenue_month,
            gross_revenue,
            monthly_orders,
            monthly_customers,
            average_order_value,
            units_sold
        FROM insightpilot_processed_db.revenue_features
        ORDER BY revenue_month
    """

    result = AthenaService().execute_query(
        query=query,
        timeout_seconds=60,
        max_results=5000,
    )

    rows = _extract_rows(result)

    if not rows:
        raise ValueError(
            "Athena returned no rows from revenue_features."
        )

    dataframe = pd.DataFrame(rows)

    missing_columns = (
        set(selected_columns)
        - set(dataframe.columns)
    )

    if missing_columns:
        raise ValueError(
            "Missing revenue columns: "
            f"{sorted(missing_columns)}"
        )

    dataframe[DATE_COLUMN] = pd.to_datetime(
        dataframe[DATE_COLUMN],
        errors="coerce",
    )

    numeric_columns = [
        TARGET_COLUMN,
        *BASE_FEATURE_COLUMNS,
    ]

    for column in numeric_columns:
        dataframe[column] = pd.to_numeric(
            dataframe[column],
            errors="coerce",
        )

    dataframe = dataframe.dropna(
        subset=[
            DATE_COLUMN,
            TARGET_COLUMN,
        ]
    )

    dataframe = (
        dataframe
        .sort_values(DATE_COLUMN)
        .drop_duplicates(
            subset=[DATE_COLUMN],
            keep="last",
        )
        .reset_index(drop=True)
    )

    if len(dataframe) <= 12:
        raise ValueError(
            "Revenue forecasting requires more than "
            "12 monthly observations."
        )

    return dataframe