from __future__ import annotations

from agents.nodes.common import (
    add_agent,
    add_error,
)
from agents.state import AgentState


def data_quality_agent_node(
    state: AgentState,
) -> AgentState:
    try:
        result = {
            "status": "available",
            "message": (
                "Read the latest Phase 4 data-quality report "
                "using the existing quality-report service."
            ),
        }

        return {
            "quality_result": result,
            "agents_used": add_agent(
                state,
                "data_quality_agent",
            ),
        }

    except RuntimeError as exc:
        return {
            "errors": add_error(
                state,
                f"Data Quality Agent: {exc}",
            ),
            "agents_used": add_agent(
                state,
                "data_quality_agent",
            ),
        }