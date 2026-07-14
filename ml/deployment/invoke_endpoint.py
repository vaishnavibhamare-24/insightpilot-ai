from __future__ import annotations

import json

from backend.config.settings import get_settings
from backend.services.aws_session import get_aws_session

settings = get_settings()


SAMPLE_PAYLOAD = {
    "total_orders": 6,
    "lifetime_revenue": 850.50,
    "average_order_value": 141.75,
    "days_since_last_order": 120,
    "customer_lifetime_days": 540,
    "purchase_frequency": 0.0111,
    "estimated_clv": 1700.00,
}


def invoke_endpoint() -> None:
    session = get_aws_session()

    runtime_client = session.client(
        "sagemaker-runtime"
    )

    response = runtime_client.invoke_endpoint(
        EndpointName=(
            settings.sagemaker_churn_endpoint_name
        ),
        ContentType="application/json",
        Accept="application/json",
        Body=json.dumps(SAMPLE_PAYLOAD),
    )

    response_body = (
        response["Body"]
        .read()
        .decode("utf-8")
    )

    print(
        json.dumps(
            json.loads(response_body),
            indent=2,
        )
    )


if __name__ == "__main__":
    invoke_endpoint()