from __future__ import annotations

from typing import Any

from pydantic import BaseModel


class LivenessResponse(BaseModel):
    status: str
    service: str
    version: str


class DependencyStatus(BaseModel):
    name: str
    status: str
    latency_ms: float | None = None
    detail: str | None = None


class ReadinessResponse(BaseModel):
    status: str
    dependencies: list[DependencyStatus]


class DetailedHealthResponse(BaseModel):
    status: str
    service: str
    version: str
    environment: str
    dependencies: list[DependencyStatus]
    metadata: dict[str, Any]