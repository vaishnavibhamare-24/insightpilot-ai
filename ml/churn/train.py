from __future__ import annotations

import json

import joblib
import mlflow
import mlflow.xgboost
import pandas as pd
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier

from ml.churn.config import (
    ARTIFACT_DIR,
    FEATURE_COLUMNS,
    FEATURE_IMPORTANCE_PATH,
    METRICS_PATH,
    MODEL_PATH,
    RANDOM_STATE,
    TARGET_COLUMN,
    TEST_SIZE,
)
from ml.churn.data_loader import load_churn_data
from ml.churn.feature_builder import build_churn_features
from ml.common.metrics import classification_metrics
from ml.common.mlflow_utils import configure_mlflow


def train_churn_model() -> None:
    ARTIFACT_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    configure_mlflow()

    dataframe = load_churn_data()

    features, target = build_churn_features(
        dataframe
    )

    (
        x_train,
        x_test,
        y_train,
        y_test,
    ) = train_test_split(
        features,
        target,
        test_size=TEST_SIZE,
        random_state=RANDOM_STATE,
        stratify=target,
    )

    negative_count = int(
        (y_train == 0).sum()
    )

    positive_count = int(
        (y_train == 1).sum()
    )

    scale_pos_weight = (
        negative_count / positive_count
        if positive_count > 0
        else 1.0
    )

    model = XGBClassifier(
        n_estimators=300,
        max_depth=5,
        learning_rate=0.05,
        subsample=0.8,
        colsample_bytree=0.8,
        objective="binary:logistic",
        eval_metric="logloss",
        scale_pos_weight=scale_pos_weight,
        random_state=RANDOM_STATE,
        n_jobs=-1,
    )

    mlflow.set_experiment(
        "insightpilot-churn"
    )

    with mlflow.start_run():
        model.fit(
            x_train,
            y_train,
        )

        predictions = model.predict(
            x_test
        )

        probabilities = model.predict_proba(
            x_test
        )[:, 1]

        metrics = classification_metrics(
            y_true=y_test,
            y_pred=predictions,
            y_probability=probabilities,
        )

        mlflow.log_params(
            model.get_params()
        )

        mlflow.log_param(
            "feature_count",
            len(FEATURE_COLUMNS),
        )

        mlflow.log_param(
            "training_rows",
            len(x_train),
        )

        mlflow.log_param(
            "test_rows",
            len(x_test),
        )

        mlflow.log_param(
            "negative_training_rows",
            negative_count,
        )

        mlflow.log_param(
            "positive_training_rows",
            positive_count,
        )

        for name, value in metrics.items():
            if name != "confusion_matrix":
                mlflow.log_metric(
                    name,
                    value,
                )

        artifact = {
            "model": model,
            "feature_columns": FEATURE_COLUMNS,
            "target_column": TARGET_COLUMN,
            "model_type": "XGBClassifier",
        }

        joblib.dump(
            artifact,
            MODEL_PATH,
        )

        with METRICS_PATH.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                metrics,
                file,
                indent=2,
            )

        feature_importance = pd.DataFrame(
            {
                "feature": FEATURE_COLUMNS,
                "importance": model.feature_importances_,
            }
        ).sort_values(
            by="importance",
            ascending=False,
        )

        feature_importance.to_csv(
            FEATURE_IMPORTANCE_PATH,
            index=False,
        )

        mlflow.log_artifact(
            str(MODEL_PATH)
        )

        mlflow.log_artifact(
            str(METRICS_PATH)
        )

        mlflow.log_artifact(
            str(FEATURE_IMPORTANCE_PATH)
        )

        mlflow.xgboost.log_model(
            model,
            artifact_path="model",
        )

    print()
    print("Churn model training completed.")
    print(f"Rows loaded: {len(dataframe)}")
    print(f"Training rows: {len(x_train)}")
    print(f"Test rows: {len(x_test)}")
    print(f"Model saved to: {MODEL_PATH}")
    print(f"Metrics saved to: {METRICS_PATH}")
    print()
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    train_churn_model()