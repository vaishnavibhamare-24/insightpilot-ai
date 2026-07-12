from typing import Any

from pydantic import BaseModel


class DataQualityReportResponse(BaseModel):
    generated_at: str
    overall_score: float
    status: str
    total_rules: int
    passed_rules: int
    failed_rules: int
    failed_records: int
    rules: list[dict[str, Any]]