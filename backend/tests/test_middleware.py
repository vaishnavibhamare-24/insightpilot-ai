from __future__ import annotations


def test_request_id_is_generated(
    client,
) -> None:
    response = client.get(
        "/api/v1/health/live"
    )

    assert response.status_code == 200
    assert "X-Request-ID" in response.headers

    request_id = response.headers[
        "X-Request-ID"
    ]

    assert request_id


def test_existing_request_id_is_preserved(
    client,
) -> None:
    request_id = "insightpilot-test-request"

    response = client.get(
        "/api/v1/health/live",
        headers={
            "X-Request-ID": request_id,
        },
    )

    assert response.status_code == 200

    assert (
        response.headers["X-Request-ID"]
        == request_id
    )


def test_process_time_header_exists(
    client,
) -> None:
    response = client.get(
        "/api/v1/health/live"
    )

    assert response.status_code == 200

    process_time = response.headers[
        "X-Process-Time-MS"
    ]

    assert float(process_time) >= 0