import pandas as pd

from ml.churn.config import FEATURE_COLUMNS
from ml.churn.feature_builder import build_churn_features


def test_churn_feature_builder() -> None:
    dataframe = pd.DataFrame(
        [
            {
                "total_orders": 3,
                "lifetime_revenue": 1000.0,
                "average_order_value": 333.33,
                "days_since_last_order": 90,
                "customer_lifetime_days": 500,
                "purchase_frequency": 0.006,
                "estimated_clv": 1200.0,
                "churn_label": 1,
            },
            {
                "total_orders": 10,
                "lifetime_revenue": 5000.0,
                "average_order_value": 500.0,
                "days_since_last_order": 10,
                "customer_lifetime_days": 900,
                "purchase_frequency": 0.011,
                "estimated_clv": 5500.0,
                "churn_label": 0,
            },
        ]
    )

    features, target = build_churn_features(dataframe)

    assert list(features.columns) == FEATURE_COLUMNS
    assert not features.isnull().any().any()
    assert set(target.unique()).issubset({0, 1})