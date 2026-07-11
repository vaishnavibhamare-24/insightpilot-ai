from typing import Any

from pydantic import BaseModel, Field, field_validator


class AthenaQueryRequest(BaseModel):
    query: str = Field(
        min_length=1,
        max_length=10_000,
        description="Read-only Athena SQL query.",
        examples=[
            "SELECT COUNT(*) AS total FROM customers"
        ],
    )
    timeout_seconds: int = Field(
        default=30,
        ge=5,
        le=120,
        description="Maximum time to wait for Athena.",
    )
    max_results: int = Field(
        default=1000,
        ge=1,
        le=5000,
        description="Maximum number of result rows returned.",
    )

    @field_validator("query")
    @classmethod
    def query_cannot_be_blank(cls, value: str) -> str:
        query = value.strip()

        if not query:
            raise ValueError("Query cannot be blank.")

        return query


class AthenaQueryStatistics(BaseModel):
    engine_execution_time_ms: int | None = None
    data_scanned_bytes: int | None = None
    total_execution_time_ms: int | None = None


class AthenaQueryResponse(BaseModel):
    query_execution_id: str
    status: str
    columns: list[str]
    rows: list[dict[str, Any]]
    row_count: int = Field(ge=0)
    statistics: AthenaQueryStatistics