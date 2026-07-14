from __future__ import annotations

import time

from botocore.exceptions import ClientError
from sagemaker.core import image_uris

from backend.config.settings import get_settings
from backend.services.aws_session import get_aws_session


settings = get_settings()


MODEL_DATA_URL = (
    f"s3://{settings.s3_processed_bucket}"
    "/models/churn/model.tar.gz"
)


def wait_for_endpoint(
    client,
    endpoint_name: str,
    timeout_minutes: int = 20,
) -> None:
    deadline = time.monotonic() + (
        timeout_minutes * 60
    )

    while time.monotonic() < deadline:
        response = client.describe_endpoint(
            EndpointName=endpoint_name
        )

        status = response["EndpointStatus"]

        print(f"Endpoint status: {status}")

        if status == "InService":
            return

        if status == "Failed":
            reason = response.get(
                "FailureReason",
                "Unknown deployment failure.",
            )

            raise RuntimeError(reason)

        time.sleep(30)

    raise TimeoutError(
        "SageMaker endpoint deployment timed out."
    )


def check_existing_endpoint(client) -> None:
    try:
        client.describe_endpoint(
            EndpointName=(
                settings.sagemaker_churn_endpoint_name
            )
        )

        raise RuntimeError(
            "The endpoint already exists. "
            "Delete it before redeploying."
        )

    except ClientError as exc:
        error_code = (
            exc.response
            .get("Error", {})
            .get("Code")
        )

        if error_code != "ValidationException":
            raise


def deploy_churn_endpoint() -> None:
    session = get_aws_session()

    client = session.client(
        "sagemaker"
    )

    check_existing_endpoint(client)

    xgboost_image = image_uris.retrieve(
        framework="xgboost",
        region=settings.aws_region,
        version="3.0-5",
        py_version="py3",
        instance_type=(
            settings.sagemaker_instance_type
        ),
        image_scope="inference",
    )

    print(
        f"Inference image: {xgboost_image}"
    )

    client.create_model(
        ModelName=(
            settings.sagemaker_model_name
        ),
        PrimaryContainer={
            "Image": xgboost_image,
            "ModelDataUrl": MODEL_DATA_URL,
            "Environment": {
                "SAGEMAKER_PROGRAM": (
                    "inference.py"
                ),
                "SAGEMAKER_SUBMIT_DIRECTORY": (
                    "/opt/ml/model/code"
                ),
            },
        },
        ExecutionRoleArn=(
            settings.sagemaker_role_arn
        ),
    )

    capture_destination = (
        f"s3://{settings.s3_processed_bucket}/"
        f"{settings.sagemaker_capture_prefix}/"
    )

    client.create_endpoint_config(
        EndpointConfigName=(
            settings
            .sagemaker_endpoint_config_name
        ),
        ProductionVariants=[
            {
                "VariantName": "AllTraffic",
                "ModelName": (
                    settings.sagemaker_model_name
                ),
                "InitialInstanceCount": 1,
                "InstanceType": (
                    settings.sagemaker_instance_type
                ),
                "InitialVariantWeight": 1.0,
            }
        ],
        DataCaptureConfig={
            "EnableCapture": True,
            "InitialSamplingPercentage": 100,
            "DestinationS3Uri": (
                capture_destination
            ),
            "CaptureOptions": [
                {
                    "CaptureMode": "Input"
                },
                {
                    "CaptureMode": "Output"
                },
            ],
            "CaptureContentTypeHeader": {
                "JsonContentTypes": [
                    "application/json"
                ]
            },
        },
    )

    client.create_endpoint(
        EndpointName=(
            settings
            .sagemaker_churn_endpoint_name
        ),
        EndpointConfigName=(
            settings
            .sagemaker_endpoint_config_name
        ),
    )

    wait_for_endpoint(
        client=client,
        endpoint_name=(
            settings
            .sagemaker_churn_endpoint_name
        ),
    )

    print(
        "Churn endpoint is InService."
    )


if __name__ == "__main__":
    deploy_churn_endpoint()