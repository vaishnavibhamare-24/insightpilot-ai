from __future__ import annotations

import pandas as pd

from ml.forecasting.config import (
    DATE_COLUMN,
    TARGET_COLUMN,
)


def build_forecast_features(
    dataframe: pd.DataFrame,
) -> pd.DataFrame:
    data = dataframe.copy()

    data[DATE_COLUMN] = pd.to_datetime(
        data[DATE_COLUMN],
        errors="coerce",
    )

    data = (
        data
        .dropna(subset=[DATE_COLUMN])
        .sort_values(DATE_COLUMN)
        .reset_index(drop=True)
    )

    data["year"] = (
        data[DATE_COLUMN].dt.year
    )

    data["month"] = (
        data[DATE_COLUMN].dt.month
    )

    data["quarter"] = (
        data[DATE_COLUMN].dt.quarter
    )

    data["revenue_lag_1"] = (
        data[TARGET_COLUMN].shift(1)
    )

    data["revenue_lag_2"] = (
        data[TARGET_COLUMN].shift(2)
    )

    data["revenue_lag_3"] = (
        data[TARGET_COLUMN].shift(3)
    )

    data["revenue_rolling_mean_3"] = (
        data[TARGET_COLUMN]
        .shift(1)
        .rolling(window=3)
        .mean()
    )

    data["revenue_rolling_mean_6"] = (
        data[TARGET_COLUMN]
        .shift(1)
        .rolling(window=6)
        .mean()
    )

    data = data.dropna().reset_index(
        drop=True
    )

    return data