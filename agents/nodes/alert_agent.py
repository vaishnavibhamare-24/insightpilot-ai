from __future__ import annotations

from agents.nodes.common import add_agent
from agents.state import AgentState


def alert_agent_node(
    state: AgentState,
) -> AgentState:
    quality = state.get("quality_result") or {}
    ml_result = state.get("ml_result") or {}

    severity = "info"
    triggered = False
    reasons: list[str] = []

    quality_score = quality.get("quality_score")

    if isinstance(quality_score, (int, float)):
        if quality_score < 90:
            triggered = True
            severity = "high"
            reasons.append(
                "Data-quality score is below 90."
            )

    churn_probability = ml_result.get(
        "churn_probability"
    )

    if isinstance(
        churn_probability,
        (int, float),
    ):
        if churn_probability >= 0.70:
            triggered = True
            severity = "high"
            reasons.append(
                "Churn probability is at least 0.70."
            )

    return {
        "alert_result": {
            "triggered": triggered,
            "severity": severity,
            "reasons": reasons,
        },
        "agents_used": add_agent(
            state,
            "alert_agent",
        ),
    }