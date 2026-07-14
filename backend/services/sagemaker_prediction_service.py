from __future__ import annotations

import json
import logging
import time
from typing import Any

from botocore.exceptions import (
    BotoCoreError,
    ClientError,
)

from backend.config.settings import get_settings
from backend.services.aws_session import get_aws_session


logger = logging.getLogger(__name__)
settings = get_settings()


class SageMakerPredictionError(RuntimeError):
    pass


class SageMakerPredictionService:
    def __init__(self) -> None:
        session = get_aws_session()

        self.client = session.client(
            "sagemaker-runtime"
        )

    def predict_churn(
        self,
        features: dict[str, Any],
    ) -> dict[str, Any]:
        start_time = time.perf_counter()

        try:
            response = self.client.invoke_endpoint(
                EndpointName=(
                    settings
                    .sagemaker_churn_endpoint_name
                ),
                ContentType="application/json",
                Accept="application/json",
                Body=json.dumps(features),
            )

            raw_body = (
                response["Body"]
                .read()
                .decode("utf-8")
            )

            result = json.loads(raw_body)

            latency_ms = (
                time.perf_counter() - start_time
            ) * 1000

            logger.info(
                "SageMaker churn prediction succeeded. "
                "endpoint=%s latency_ms=%.2f "
                "prediction=%s probability=%s",
                settings.sagemaker_churn_endpoint_name,
                latency_ms,
                result.get("churn_prediction"),
                result.get("churn_probability"),
            )

            result["endpoint_name"] = (
                settings
                .sagemaker_churn_endpoint_name
            )

            result["latency_ms"] = round(
                latency_ms,
                2,
            )

            return result

        except ClientError as exc:
            error = exc.response.get(
                "Error",
                {}
            )

            code = error.get(
                "Code",
                "Unknown",
            )

            message = error.get(
                "Message",
                "Endpoint invocation failed.",
            )

            raise SageMakerPredictionError(
                f"SageMaker error {code}: {message}"
            ) from exc

        except (
            BotoCoreError,
            json.JSONDecodeError,
        ) as exc:
            raise SageMakerPredictionError(
                "Unable to invoke the SageMaker "
                "churn endpoint."
            ) from exc