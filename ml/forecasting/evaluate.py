from __future__ import annotations

import json
import shutil

import matplotlib.pyplot as plt
import pandas as pd

from ml.forecasting.config import (
    ARIMA_METRICS_PATH,
    ARIMA_MODEL_PATH,
    ARTIFACT_DIR,
    BEST_MODEL_PATH,
    COMPARISON_PATH,
    FORECAST_PLOT_PATH,
    XGBOOST_METRICS_PATH,
    XGBOOST_MODEL_PATH,
)


def _load_json(path):
    if not path.exists():
        raise FileNotFoundError(
            f"Required file not found: {path}"
        )

    with path.open(
        "r",
        encoding="utf-8",
    ) as file:
        return json.load(file)


def compare_forecast_models() -> None:
    xgboost_metrics = _load_json(
        XGBOOST_METRICS_PATH
    )

    arima_metrics = _load_json(
        ARIMA_METRICS_PATH
    )

    comparison = pd.DataFrame(
        [
            {
                "model": "xgboost",
                "mae": xgboost_metrics["mae"],
                "rmse": xgboost_metrics["rmse"],
                "mape": xgboost_metrics["mape"],
                "r2": xgboost_metrics["r2"],
            },
            {
                "model": "arima",
                "mae": arima_metrics["mae"],
                "rmse": arima_metrics["rmse"],
                "mape": arima_metrics["mape"],
                "r2": arima_metrics["r2"],
            },
        ]
    )

    comparison.to_csv(
        COMPARISON_PATH,
        index=False,
    )

    ranked = comparison.sort_values(
        by=[
            "rmse",
            "mape",
            "mae",
        ],
        ascending=True,
    )

    best_row = ranked.iloc[0]

    best_model_name = str(
        best_row["model"]
    )

    if best_model_name == "xgboost":
        source_model_path = (
            XGBOOST_MODEL_PATH
        )
    else:
        source_model_path = (
            ARIMA_MODEL_PATH
        )

    selected_model_path = (
        ARTIFACT_DIR
        / "revenue_model.joblib"
    )

    shutil.copy2(
        source_model_path,
        selected_model_path,
    )

    best_model_output = {
        "model_name": best_model_name,
        "reason": (
            "Selected using the lowest RMSE, "
            "with MAPE and MAE used as "
            "secondary comparison metrics."
        ),
        "mae": float(best_row["mae"]),
        "rmse": float(best_row["rmse"]),
        "mape": float(best_row["mape"]),
        "r2": float(best_row["r2"]),
        "selected_model_path": str(
            selected_model_path
        ),
    }

    with BEST_MODEL_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            best_model_output,
            file,
            indent=2,
        )

    xgb_predictions = pd.read_csv(
        ARTIFACT_DIR
        / "xgboost_test_predictions.csv"
    )

    arima_predictions = pd.read_csv(
        ARTIFACT_DIR
        / "arima_test_predictions.csv"
    )

    dates = pd.to_datetime(
        xgb_predictions["revenue_month"]
    )

    plt.figure(figsize=(10, 6))

    plt.plot(
        dates,
        xgb_predictions["actual_revenue"],
        marker="o",
        label="Actual",
    )

    plt.plot(
        dates,
        xgb_predictions["predicted_revenue"],
        marker="o",
        label="XGBoost",
    )

    plt.plot(
        dates,
        arima_predictions["predicted_revenue"],
        marker="o",
        label="ARIMA",
    )

    plt.xlabel("Revenue month")
    plt.ylabel("Revenue")
    plt.title(
        "Revenue Forecast Model Comparison"
    )
    plt.legend()
    plt.xticks(rotation=45)
    plt.tight_layout()

    plt.savefig(
        FORECAST_PLOT_PATH,
        dpi=200,
        bbox_inches="tight",
    )

    plt.close()

    print()
    print("Forecast model comparison")
    print("=========================")
    print(
        comparison.to_string(
            index=False
        )
    )
    print()
    print(
        f"Selected model: "
        f"{best_model_name}"
    )
    print(
        f"Selected artifact: "
        f"{selected_model_path}"
    )
    print(
        f"Best model JSON: "
        f"{BEST_MODEL_PATH}"
    )


if __name__ == "__main__":
    compare_forecast_models()