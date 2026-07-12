from __future__ import annotations

import json
import warnings

import joblib
import mlflow
import numpy as np
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA

from ml.common.metrics import regression_metrics
from ml.common.mlflow_utils import configure_mlflow
from ml.forecasting.config import (
    ARIMA_METRICS_PATH,
    ARIMA_MODEL_PATH,
    ARTIFACT_DIR,
    DATE_COLUMN,
    TARGET_COLUMN,
    TEST_MONTHS,
)
from ml.forecasting.data_loader import (
    load_revenue_data,
)


ARIMA_ORDERS = [
    (1, 1, 1),
    (2, 1, 1),
    (1, 1, 2),
]


def train_arima_forecast() -> None:
    warnings.filterwarnings(
        "ignore"
    )

    ARTIFACT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    configure_mlflow()

    dataframe = load_revenue_data()

    train_data = dataframe.iloc[
        :-TEST_MONTHS
    ].copy()

    test_data = dataframe.tail(
        TEST_MONTHS
    ).copy()

    train_series = train_data[
        TARGET_COLUMN
    ].astype(float)

    test_series = test_data[
        TARGET_COLUMN
    ].astype(float)

    best_result = None

    mlflow.set_experiment(
        "insightpilot-revenue-forecast"
    )

    for order in ARIMA_ORDERS:
        print(
            f"Training ARIMA order {order}..."
        )

        try:
            fitted_model = ARIMA(
                train_series,
                order=order,
            ).fit()

            forecast = fitted_model.forecast(
                steps=len(test_series)
            )

            forecast_values = np.asarray(
                forecast,
                dtype=float,
            )

            metrics = regression_metrics(
                y_true=test_series.to_numpy(),
                y_pred=forecast_values,
            )

            candidate = {
                "order": order,
                "model": fitted_model,
                "predictions": forecast_values,
                "metrics": metrics,
            }

            if (
                best_result is None
                or metrics["rmse"]
                < best_result["metrics"]["rmse"]
            ):
                best_result = candidate

        except Exception as exc:
            print(
                f"ARIMA {order} failed: {exc}"
            )

    if best_result is None:
        raise RuntimeError(
            "All ARIMA configurations failed."
        )

    best_order = best_result["order"]
    best_model = best_result["model"]
    best_predictions = best_result[
        "predictions"
    ]
    best_metrics = best_result["metrics"]

    with mlflow.start_run(
        run_name="arima-revenue"
    ):
        mlflow.log_param(
            "order",
            str(best_order),
        )

        mlflow.log_param(
            "training_months",
            len(train_data),
        )

        mlflow.log_param(
            "test_months",
            len(test_data),
        )

        for name, value in best_metrics.items():
            mlflow.log_metric(
                name,
                value,
            )

        artifact = {
            "model": best_model,
            "model_name": "arima",
            "order": best_order,
            "date_column": DATE_COLUMN,
            "target_column": TARGET_COLUMN,
            "last_training_date": str(
                dataframe[DATE_COLUMN].max().date()
            ),
            "history": dataframe.to_dict(
                orient="records"
            ),
        }

        joblib.dump(
            artifact,
            ARIMA_MODEL_PATH,
        )

        metrics_output = {
            "order": list(best_order),
            **best_metrics,
        }

        with ARIMA_METRICS_PATH.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                metrics_output,
                file,
                indent=2,
            )

        prediction_output = pd.DataFrame(
            {
                DATE_COLUMN: test_data[
                    DATE_COLUMN
                ].dt.strftime("%Y-%m-%d"),
                "actual_revenue": (
                    test_series.to_numpy()
                ),
                "predicted_revenue": (
                    best_predictions
                ),
            }
        )

        prediction_path = (
            ARTIFACT_DIR
            / "arima_test_predictions.csv"
        )

        prediction_output.to_csv(
            prediction_path,
            index=False,
        )

        mlflow.log_artifact(
            str(ARIMA_MODEL_PATH)
        )

        mlflow.log_artifact(
            str(ARIMA_METRICS_PATH)
        )

        mlflow.log_artifact(
            str(prediction_path)
        )

    print()
    print("ARIMA revenue training completed.")
    print(f"Best ARIMA order: {best_order}")
    print(
        f"Model saved to: "
        f"{ARIMA_MODEL_PATH}"
    )
    print(
        json.dumps(
            {
                "order": list(best_order),
                **best_metrics,
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    train_arima_forecast()