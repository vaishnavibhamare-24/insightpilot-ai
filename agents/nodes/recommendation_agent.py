from __future__ import annotations

import json

from agents.nodes.common import (
    add_agent,
    add_error,
)
from agents.services.bedrock_chat_service import (
    BedrockChatError,
    BedrockChatService,
)
from agents.state import AgentState


def recommendation_agent_node(
    state: AgentState,
) -> AgentState:
    try:
        context = {
            "sql_result": state.get("sql_result"),
            "ml_result": state.get("ml_result"),
            "quality_result": state.get(
                "quality_result"
            ),
            "root_cause_result": state.get(
                "root_cause_result"
            ),
        }

        prompt = f"""
Question:
{state["message"]}

Analysis:
{json.dumps(context, default=str)}

Provide three practical business recommendations.

Return each recommendation on a separate line.
Do not include unsupported claims.
"""

        text = BedrockChatService().generate(
            prompt=prompt,
            system_prompt=(
                "You provide concise, evidence-based "
                "business recommendations."
            ),
            max_tokens=500,
            temperature=0.2,
        )

        recommendations = [
            line.lstrip("-•1234567890. ").strip()
            for line in text.splitlines()
            if line.strip()
        ][:5]

        return {
            "recommendation_result": recommendations,
            "agents_used": add_agent(
                state,
                "recommendation_agent",
            ),
        }

    except (
        BedrockChatError,
        RuntimeError,
    ) as exc:
        return {
            "errors": add_error(
                state,
                f"Recommendation Agent: {exc}",
            ),
            "agents_used": add_agent(
                state,
                "recommendation_agent",
            ),
        }