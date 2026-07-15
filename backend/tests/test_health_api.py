from __future__ import annotations

from unittest.mock import patch


def test_liveness_endpoint(
    client,
):
    response = client.get(
        "/api/v1/health/live"
    )

    assert response.status_code == 200

    body = response.json()

    assert body["status"] == "alive"
    assert body["service"] == "InsightPilot AI"

    assert "X-Request-ID" in response.headers
    assert "X-Process-Time-MS" in response.headers


@patch(
    "backend.api.v1.health.HealthService.readiness"
)
def test_readiness_endpoint(
    mock_readiness,
    client,
):
    mock_readiness.return_value = {
        "status": "ready",
        "dependencies": [
            {
                "name": "aws_sts",
                "status": "healthy",
                "latency_ms": 10.0,
                "detail": None,
            },
        ],
    }

    response = client.get(
        "/api/v1/health/ready"
    )

    assert response.status_code == 200
    assert response.json()["status"] == "ready"


@patch(
    "backend.api.v1.health.HealthService.readiness"
)
def test_readiness_failure(
    mock_readiness,
    client,
):
    mock_readiness.return_value = {
        "status": "not_ready",
        "dependencies": [
            {
                "name": "s3_raw_bucket",
                "status": "unhealthy",
                "latency_ms": 10.0,
                "detail": "Access denied",
            },
        ],
    }

    response = client.get(
        "/api/v1/health/ready"
    )

    assert response.status_code == 503
    assert (
        response.json()["status"]
        == "not_ready"
    )