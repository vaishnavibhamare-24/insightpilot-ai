from __future__ import annotations

from typing import Any, Literal, TypedDict


AgentRoute = Literal[
    "sql",
    "rag",
    "ml",
    "data_quality",
    "visualization",
    "root_cause",
    "recommendation",
    "alert",
    "general",
]


class AgentState(TypedDict, total=False):
    message: str
    session_id: str | None

    route: AgentRoute
    requested_route: AgentRoute
    route_reason: str
    confidence: float

    generated_sql: str | None
    sql_result: dict[str, Any] | None

    rag_answer: str | None
    citations: list[dict[str, Any]]

    ml_result: dict[str, Any] | None
    quality_result: dict[str, Any] | None

    root_cause_result: dict[str, Any] | None
    recommendation_result: list[str]
    alert_result: dict[str, Any] | None
    visualization: dict[str, Any] | None

    agents_used: list[str]
    errors: list[str]

    final_answer: str