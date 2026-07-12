from __future__ import annotations

import mlflow

from backend.config.settings import get_settings


def configure_mlflow() -> None:
    settings = get_settings()

    mlflow.set_tracking_uri(
        settings.mlflow_tracking_uri
    )