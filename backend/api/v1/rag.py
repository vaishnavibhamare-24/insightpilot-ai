from fastapi import APIRouter, HTTPException, status

from backend.schemas.rag import (
    RAGQueryRequest,
    RAGQueryResponse,
)
from backend.services.bedrock_rag_service import (
    BedrockRAGError,
    BedrockRAGService,
)

router = APIRouter()


@router.post(
    "/query",
    response_model=RAGQueryResponse,
    summary="Ask the InsightPilot Knowledge Base",
)
def query_knowledge_base(
    request: RAGQueryRequest,
) -> RAGQueryResponse:
    try:
        result = BedrockRAGService().query(
            question=request.question,
            session_id=request.session_id,
        )

        return RAGQueryResponse(**result)

    except BedrockRAGError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc

    except RuntimeError as exc:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=str(exc),
        ) from exc