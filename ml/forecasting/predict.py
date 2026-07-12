from __future__ import annotations

import json
from typing import Any

import joblib
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

from ml.forecasting.config import (
    BEST_MODEL_PATH,
    DATE_COLUMN,
    MODEL_FEATURE_COLUMNS,
    TARGET_COLUMN,
)


class RevenueForecaster:
    def __init__(self) -> None:
        selected_model_path = (
            BEST_MODEL_PATH.parent
            / "revenue_model.joblib"
        )

        if not BEST_MODEL_PATH.exists():
            raise FileNotFoundError(
                "best_model.json was not found. "
                "Run python -m ml.forecasting.evaluate first."
            )

        if not selected_model_path.exists():
            raise FileNotFoundError(
                "Selected revenue model was not found."
            )

        with BEST_MODEL_PATH.open(
            "r",
            encoding="utf-8",
        ) as file:
            selection = json.load(file)

        self.model_name = selection["model_name"]
        self.artifact = joblib.load(
            selected_model_path
        )

        self.history = pd.DataFrame(
            self.artifact["history"]
        )

        self.history[DATE_COLUMN] = pd.to_datetime(
            self.history[DATE_COLUMN]
        )

        self.history[TARGET_COLUMN] = pd.to_numeric(
            self.history[TARGET_COLUMN],
            errors="coerce",
        )

        self.history = (
            self.history
            .sort_values(DATE_COLUMN)
            .reset_index(drop=True)
        )

    @staticmethod
    def _safe_recent_average(
        dataframe: pd.DataFrame,
        column: str,
        window: int = 3,
    ) -> float:
        values = pd.to_numeric(
            dataframe[column],
            errors="coerce",
        ).dropna()

        if values.empty:
            return 0.0

        return float(
            values.tail(window).mean()
        )

    def _forecast_xgboost(
        self,
        months: int,
    ) -> list[dict[str, Any]]:
        model = self.artifact["model"]
        history = self.history.copy()

        predictions: list[dict[str, Any]] = []

        for _ in range(months):
            next_month = (
                history[DATE_COLUMN].max()
                + pd.offsets.MonthBegin(1)
            )

            revenue_values = (
                history[TARGET_COLUMN]
                .astype(float)
                .tolist()
            )

            lag_1 = revenue_values[-1]
            lag_2 = revenue_values[-2]
            lag_3 = revenue_values[-3]

            rolling_mean_3 = float(
                np.mean(revenue_values[-3:])
            )

            rolling_mean_6 = float(
                np.mean(revenue_values[-6:])
            )

            monthly_orders = (
                self._safe_recent_average(
                    history,
                    "monthly_orders",
                )
            )

            monthly_customers = (
                self._safe_recent_average(
                    history,
                    "monthly_customers",
                )
            )

            average_order_value = (
                self._safe_recent_average(
                    history,
                    "average_order_value",
                )
            )

            units_sold = (
                self._safe_recent_average(
                    history,
                    "units_sold",
                )
            )

            feature_row = pd.DataFrame(
                [
                    {
                        "year": next_month.year,
                        "month": next_month.month,
                        "quarter": next_month.quarter,
                        "monthly_orders": monthly_orders,
                        "monthly_customers": monthly_customers,
                        "average_order_value": (
                            average_order_value
                        ),
                        "units_sold": units_sold,
                        "revenue_lag_1": lag_1,
                        "revenue_lag_2": lag_2,
                        "revenue_lag_3": lag_3,
                        "revenue_rolling_mean_3": (
                            rolling_mean_3
                        ),
                        "revenue_rolling_mean_6": (
                            rolling_mean_6
                        ),
                    }
                ]
            )

            feature_row = feature_row[
                MODEL_FEATURE_COLUMNS
            ]

            predicted_revenue = float(
                model.predict(feature_row)[0]
            )

            predicted_revenue = max(
                predicted_revenue,
                0.0,
            )

            predictions.append(
                {
                    "month": next_month.strftime(
                        "%Y-%m"
                    ),
                    "predicted_revenue": round(
                        predicted_revenue,
                        2,
                    ),
                }
            )

            new_history_row = {
                DATE_COLUMN: next_month,
                TARGET_COLUMN: predicted_revenue,
                "monthly_orders": monthly_orders,
                "monthly_customers": (
                    monthly_customers
                ),
                "average_order_value": (
                    average_order_value
                ),
                "units_sold": units_sold,
            }

            history = pd.concat(
                [
                    history,
                    pd.DataFrame(
                        [new_history_row]
                    ),
                ],
                ignore_index=True,
            )

        return predictions

    def _forecast_arima(
        self,
        months: int,
    ) -> list[dict[str, Any]]:
        order = tuple(
            self.artifact.get(
                "order",
                (1, 1, 1),
            )
        )

        full_series = (
            self.history[TARGET_COLUMN]
            .astype(float)
        )

        fitted_model = ARIMA(
            full_series,
            order=order,
        ).fit()

        forecast_values = fitted_model.forecast(
            steps=months
        )

        last_month = self.history[
            DATE_COLUMN
        ].max()

        predictions = []

        for index, value in enumerate(
            forecast_values,
            start=1,
        ):
            forecast_month = (
                last_month
                + pd.offsets.MonthBegin(index)
            )

            predictions.append(
                {
                    "month": (
                        forecast_month.strftime(
                            "%Y-%m"
                        )
                    ),
                    "predicted_revenue": round(
                        max(float(value), 0.0),
                        2,
                    ),
                }
            )

        return predictions

    def forecast(
        self,
        months: int,
    ) -> dict[str, Any]:
        if months < 1 or months > 12:
            raise ValueError(
                "Forecast months must be between 1 and 12."
            )

        if self.model_name == "xgboost":
            predictions = (
                self._forecast_xgboost(months)
            )
        elif self.model_name == "arima":
            predictions = (
                self._forecast_arima(months)
            )
        else:
            raise ValueError(
                "Unsupported selected forecast model: "
                f"{self.model_name}"
            )

        return {
            "forecast_horizon": months,
            "model_name": self.model_name,
            "predictions": predictions,
        }