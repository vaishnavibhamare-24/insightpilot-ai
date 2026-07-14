from __future__ import annotations

from typing import Any

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    message: str = Field(
        min_length=3,
        max_length=3000,
    )
    session_id: str | None = None


class ChatResponse(BaseModel):
    answer: str
    route: str | None = None
    route_reason: str | None = None
    confidence: float | None = None
    agents_used: list[str]

    generated_sql: str | None = None
    data: dict[str, Any] | None = None

    citations: list[dict[str, Any]]
    visualization: dict[str, Any] | None = None
    recommendations: list[str]
    alert: dict[str, Any] | None = None

    errors: list[str]
    session_id: str
    latency_ms: float