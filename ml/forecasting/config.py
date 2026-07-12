from pathlib import Path

DATE_COLUMN = "revenue_month"
TARGET_COLUMN = "gross_revenue"

BASE_FEATURE_COLUMNS = [
    "monthly_orders",
    "monthly_customers",
    "average_order_value",
    "units_sold",
]

MODEL_FEATURE_COLUMNS = [
    "year",
    "month",
    "quarter",
    "monthly_orders",
    "monthly_customers",
    "average_order_value",
    "units_sold",
    "revenue_lag_1",
    "revenue_lag_2",
    "revenue_lag_3",
    "revenue_rolling_mean_3",
    "revenue_rolling_mean_6",
]

TEST_MONTHS = 6
RANDOM_STATE = 42

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ARTIFACT_DIR = (
    PROJECT_ROOT
    / "ml"
    / "artifacts"
    / "forecasting"
)

XGBOOST_MODEL_PATH = (
    ARTIFACT_DIR
    / "revenue_xgboost_model.joblib"
)

ARIMA_MODEL_PATH = (
    ARTIFACT_DIR
    / "revenue_arima_model.joblib"
)

XGBOOST_METRICS_PATH = (
    ARTIFACT_DIR
    / "xgboost_metrics.json"
)

ARIMA_METRICS_PATH = (
    ARTIFACT_DIR
    / "arima_metrics.json"
)

COMPARISON_PATH = (
    ARTIFACT_DIR
    / "model_comparison.csv"
)

BEST_MODEL_PATH = (
    ARTIFACT_DIR
    / "best_model.json"
)

FORECAST_PLOT_PATH = (
    ARTIFACT_DIR
    / "forecast_comparison.png"
)