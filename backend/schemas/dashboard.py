from __future__ import annotations

from pydantic import BaseModel


class DashboardKPI(BaseModel):
    name: str
    value: float | int | str | None
    unit: str | None = None


class DashboardMetricsResponse(BaseModel):
    kpis: list[DashboardKPI]
    source: str