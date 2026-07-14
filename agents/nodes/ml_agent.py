from __future__ import annotations

from agents.nodes.common import (
    add_agent,
    add_error,
)
from agents.state import AgentState


def ml_agent_node(
    state: AgentState,
) -> AgentState:
    message = state["message"].lower()

    try:
        if "forecast" in message:
            return {
                "ml_result": {
                    "task": "revenue_forecast",
                    "message": (
                        "Use the revenue forecast service "
                        "created in Phase 5."
                    ),
                },
                "agents_used": add_agent(
                    state,
                    "ml_agent",
                ),
            }

        return {
            "ml_result": {
                "task": "churn_prediction",
                "message": (
                    "A churn prediction requires structured "
                    "customer feature values."
                ),
            },
            "agents_used": add_agent(
                state,
                "ml_agent",
            ),
        }

    except RuntimeError as exc:
        return {
            "errors": add_error(
                state,
                f"ML Agent: {exc}",
            ),
            "agents_used": add_agent(
                state,
                "ml_agent",
            ),
        }