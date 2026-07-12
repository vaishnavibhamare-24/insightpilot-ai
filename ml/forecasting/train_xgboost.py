from __future__ import annotations

import json

import joblib
import mlflow
import pandas as pd
from xgboost import XGBRegressor

from ml.common.metrics import regression_metrics
from ml.common.mlflow_utils import configure_mlflow
from ml.forecasting.config import (
    ARTIFACT_DIR,
    DATE_COLUMN,
    MODEL_FEATURE_COLUMNS,
    RANDOM_STATE,
    TARGET_COLUMN,
    TEST_MONTHS,
    XGBOOST_METRICS_PATH,
    XGBOOST_MODEL_PATH,
)
from ml.forecasting.data_loader import (
    load_revenue_data,
)
from ml.forecasting.feature_builder import (
    build_forecast_features,
)


def train_xgboost_forecast() -> None:
    ARTIFACT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    configure_mlflow()

    raw_data = load_revenue_data()

    dataframe = build_forecast_features(
        raw_data
    )

    if len(dataframe) <= TEST_MONTHS:
        raise ValueError(
            "Not enough rows after creating lag features."
        )

    train_data = dataframe.iloc[
        :-TEST_MONTHS
    ].copy()

    test_data = dataframe.tail(
        TEST_MONTHS
    ).copy()

    x_train = train_data[
        MODEL_FEATURE_COLUMNS
    ]

    y_train = train_data[
        TARGET_COLUMN
    ]

    x_test = test_data[
        MODEL_FEATURE_COLUMNS
    ]

    y_test = test_data[
        TARGET_COLUMN
    ]

    model = XGBRegressor(
        n_estimators=300,
        max_depth=4,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="reg:squarederror",
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    mlflow.set_experiment(
        "insightpilot-revenue-forecast"
    )

    with mlflow.start_run(
        run_name="xgboost-revenue"
    ):
        model.fit(
            x_train,
            y_train,
        )

        predictions = model.predict(
            x_test
        )

        metrics = regression_metrics(
            y_true=y_test.to_numpy(),
            y_pred=predictions,
        )

        mlflow.log_params(
            model.get_params()
        )

        mlflow.log_param(
            "training_months",
            len(train_data),
        )

        mlflow.log_param(
            "test_months",
            len(test_data),
        )

        mlflow.log_param(
            "feature_count",
            len(MODEL_FEATURE_COLUMNS),
        )

        for name, value in metrics.items():
            mlflow.log_metric(
                name,
                value,
            )

        artifact = {
            "model": model,
            "model_name": "xgboost",
            "feature_columns": MODEL_FEATURE_COLUMNS,
            "date_column": DATE_COLUMN,
            "target_column": TARGET_COLUMN,
            "last_training_date": str(
                dataframe[DATE_COLUMN].max().date()
            ),
            "history": raw_data.to_dict(
                orient="records"
            ),
        }

        joblib.dump(
            artifact,
            XGBOOST_MODEL_PATH,
        )

        with XGBOOST_METRICS_PATH.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                metrics,
                file,
                indent=2,
            )

        prediction_output = pd.DataFrame(
            {
                DATE_COLUMN: test_data[
                    DATE_COLUMN
                ].dt.strftime("%Y-%m-%d"),
                "actual_revenue": y_test.to_numpy(),
                "predicted_revenue": predictions,
            }
        )

        prediction_path = (
            ARTIFACT_DIR
            / "xgboost_test_predictions.csv"
        )

        prediction_output.to_csv(
            prediction_path,
            index=False,
        )

        mlflow.log_artifact(
            str(XGBOOST_MODEL_PATH)
        )

        mlflow.log_artifact(
            str(XGBOOST_METRICS_PATH)
        )

        mlflow.log_artifact(
            str(prediction_path)
        )

    print()
    print("XGBoost revenue training completed.")
    print(f"Raw months: {len(raw_data)}")
    print(f"Usable months: {len(dataframe)}")
    print(f"Training months: {len(train_data)}")
    print(f"Testing months: {len(test_data)}")
    print(
        f"Training ended: "
        f"{train_data[DATE_COLUMN].max().date()}"
    )
    print(
        f"Testing started: "
        f"{test_data[DATE_COLUMN].min().date()}"
    )
    print(
        f"Model saved to: "
        f"{XGBOOST_MODEL_PATH}"
    )
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    train_xgboost_forecast()