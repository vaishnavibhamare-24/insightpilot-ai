from __future__ import annotations

from pydantic import BaseModel, Field


class RAGQueryRequest(BaseModel):
    question: str = Field(
        min_length=3,
        max_length=2000,
        description="Question about InsightPilot business data and rules.",
    )
    session_id: str | None = Field(
        default=None,
        description="Optional Bedrock conversation session identifier.",
    )


class RAGCitation(BaseModel):
    text: str | None = None
    source_uri: str | None = None
    document_name: str | None = None


class RAGQueryResponse(BaseModel):
    answer: str
    citations: list[RAGCitation]
    session_id: str | None = None