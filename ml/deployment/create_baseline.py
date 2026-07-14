from __future__ import annotations

from pathlib import Path

from ml.churn.data_loader import load_churn_data
from ml.churn.feature_builder import (
    build_churn_features,
)


PROJECT_ROOT = Path(__file__).resolve().parents[2]

OUTPUT_PATH = (
    PROJECT_ROOT
    / "ml"
    / "artifacts"
    / "churn"
    / "monitoring_baseline.csv"
)


def create_baseline() -> None:
    dataframe = load_churn_data()

    features, _ = build_churn_features(
        dataframe
    )

    OUTPUT_PATH.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    features.to_csv(
        OUTPUT_PATH,
        index=False,
        header=False,
    )

    print(
        f"Baseline dataset created: "
        f"{OUTPUT_PATH}"
    )


if __name__ == "__main__":
    create_baseline()