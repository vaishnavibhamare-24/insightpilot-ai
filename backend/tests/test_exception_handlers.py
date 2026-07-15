from __future__ import annotations

from backend.core.exceptions import (
    ResourceNotFoundError,
)


def test_application_error_format(
    client,
    app,
) -> None:
    @app.get("/test/not-found")
    def test_route():
        raise ResourceNotFoundError(
            "Example resource was not found."
        )

    response = client.get(
        "/test/not-found"
    )

    assert response.status_code == 404

    payload = response.json()

    assert payload["success"] is False
    assert (
        payload["error"]["code"]
        == "RESOURCE_NOT_FOUND"
    )
    assert (
        payload["error"]["message"]
        == "Example resource was not found."
    )
    assert payload["request_id"]