from __future__ import annotations

from agents.nodes.common import (
    add_agent,
    add_error,
)
from agents.state import AgentState
from backend.services.bedrock_rag_service import (
    BedrockRAGError,
    BedrockRAGService,
)


def rag_agent_node(
    state: AgentState,
) -> AgentState:
    try:
        result = BedrockRAGService().query(
            question=state["message"],
            session_id=state.get("session_id"),
        )

        return {
            "rag_answer": result["answer"],
            "citations": result.get(
                "citations",
                [],
            ),
            "session_id": result.get(
                "session_id"
            ),
            "agents_used": add_agent(
                state,
                "rag_agent",
            ),
        }

    except (
        BedrockRAGError,
        RuntimeError,
    ) as exc:
        return {
            "errors": add_error(
                state,
                f"RAG Agent: {exc}",
            ),
            "agents_used": add_agent(
                state,
                "rag_agent",
            ),
        }