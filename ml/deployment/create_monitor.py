from __future__ import annotations

from sagemaker.core import Session
from sagemaker.model_monitor import (
    DefaultModelMonitor,
)
from sagemaker.model_monitor.dataset_format import (
    DatasetFormat,
)

from backend.config.settings import get_settings
from backend.services.aws_session import get_aws_session


settings = get_settings()


BASELINE_INPUT = (
    f"s3://{settings.s3_processed_bucket}"
    "/monitoring/churn/baseline/input/"
)

BASELINE_OUTPUT = (
    f"s3://{settings.s3_processed_bucket}"
    "/monitoring/churn/baseline/output/"
)

MONITOR_OUTPUT = (
    f"s3://{settings.s3_processed_bucket}/"
    f"{settings.sagemaker_monitoring_prefix}/"
)


def create_monitor() -> None:
    boto_session = get_aws_session()

    sagemaker_session = Session(
        boto_session=boto_session
    )

    monitor = DefaultModelMonitor(
        role=settings.sagemaker_role_arn,
        instance_count=1,
        instance_type="ml.m5.xlarge",
        volume_size_in_gb=20,
        max_runtime_in_seconds=1800,
        sagemaker_session=sagemaker_session,
    )

    monitor.suggest_baseline(
        baseline_dataset=BASELINE_INPUT,
        dataset_format=DatasetFormat.csv(
            header=False
        ),
        output_s3_uri=BASELINE_OUTPUT,
        wait=True,
        logs=True,
    )

    monitor.create_monitoring_schedule(
        monitor_schedule_name=(
            "insightpilot-churn-monitor"
        ),
        endpoint_input=(
            settings.sagemaker_churn_endpoint_name
        ),
        output_s3_uri=MONITOR_OUTPUT,
        statistics=(
            f"{BASELINE_OUTPUT}statistics.json"
        ),
        constraints=(
            f"{BASELINE_OUTPUT}constraints.json"
        ),
        schedule_cron_expression=(
            "cron(0 * ? * * *)"
        ),
        enable_cloudwatch_metrics=True,
    )

    print(
        "Model Monitor baseline and schedule "
        "created successfully."
    )


if __name__ == "__main__":
    create_monitor()