from pathlib import Path

RANDOM_STATE = 42
TEST_SIZE = 0.20

TARGET_COLUMN = "churn_label"
ID_COLUMN = "customer_id"

FEATURE_COLUMNS = [
    "total_orders",
    "lifetime_revenue",
    "average_order_value",
    "days_since_last_order",
    "customer_lifetime_days",
    "purchase_frequency",
    "estimated_clv",
]

PROJECT_ROOT = Path(__file__).resolve().parents[2]

ARTIFACT_DIR = PROJECT_ROOT / "ml" / "artifacts" / "churn"

MODEL_PATH = ARTIFACT_DIR / "churn_model.joblib"
METRICS_PATH = ARTIFACT_DIR / "metrics.json"
FEATURE_IMPORTANCE_PATH = ARTIFACT_DIR / "feature_importance.csv"
SHAP_SUMMARY_PATH = ARTIFACT_DIR / "shap_summary.png"