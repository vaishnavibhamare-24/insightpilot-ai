from fastapi import (
    APIRouter,
    HTTPException,
    status,
)

from backend.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from backend.services.agent_service import (
    AgentService,
)


router = APIRouter()


@router.post(
    "",
    response_model=ChatResponse,
    summary="Ask the InsightPilot multi-agent system",
)
def chat(
    request: ChatRequest,
) -> ChatResponse:
    try:
        result = AgentService().run(
            message=request.message,
            session_id=request.session_id,
        )

        return ChatResponse(**result)

    except Exception as exc:
        raise HTTPException(
            status_code=(
                status.HTTP_503_SERVICE_UNAVAILABLE
            ),
            detail=(
                "The multi-agent workflow could not "
                "complete the request."
            ),
        ) from exc