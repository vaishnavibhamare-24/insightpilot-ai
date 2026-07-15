from __future__ import annotations

from unittest.mock import patch


def test_chat_api(
    client,
    api_headers,
) -> None:
    mock_result = {
        "answer": "Revenue increased.",
        "route": "sql",
        "route_reason": "Metric request",
        "confidence": 0.9,
        "agents_used": [
            "router_agent",
            "sql_agent",
            "summary_agent",
        ],
        "generated_sql": (
            "SELECT 1 AS value"
        ),
        "data": {
            "rows": [
                {
                    "value": "1",
                }
            ],
        },
        "citations": [],
        "visualization": None,
        "recommendations": [],
        "alert": None,
        "errors": [],
        "session_id": "test-session",
        "latency_ms": 10.0,
    }

    with patch(
        "backend.api.v1.chat.AgentService.run",
        return_value=mock_result,
    ):
        response = client.post(
            "/api/v1/chat",
            headers=api_headers,
            json={
                "message": "Show monthly revenue",
                "session_id": None,
            },
        )

    assert response.status_code == 200

    payload = response.json()

    assert payload["answer"] == "Revenue increased."
    assert payload["route"] == "sql"
    assert payload["session_id"] == "test-session"