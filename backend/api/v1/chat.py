from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    Request,
    status,
)

from backend.api.dependencies.authentication import (
    verify_api_key,
)
from backend.config.settings import get_settings
from backend.core.rate_limit import limiter
from backend.schemas.chat import (
    ChatRequest,
    ChatResponse,
)
from backend.services.agent_service import (
    AgentService,
)


router = APIRouter()
settings = get_settings()


@router.post(
    "",
    response_model=ChatResponse,
    summary="Ask the InsightPilot multi-agent system",
    dependencies=[
        Depends(verify_api_key),
    ],
)
@limiter.limit(
    settings.rate_limit_chat
)
def chat(
    request: Request,
    payload: ChatRequest,
) -> ChatResponse:
    try:
        result = AgentService().run(
            message=payload.message,
            session_id=payload.session_id,
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