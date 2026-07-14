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


def summary_agent_node(
    state: AgentState,
) -> AgentState:
    if state.get("rag_answer"):
        base_answer = state["rag_answer"]
    else:
        base_answer = None

    context = {
        "question": state["message"],
        "route": state.get("route"),
        "sql": state.get("generated_sql"),
        "sql_result": state.get("sql_result"),
        "rag_answer": base_answer,
        "ml_result": state.get("ml_result"),
        "quality_result": state.get(
            "quality_result"
        ),
        "root_cause": state.get(
            "root_cause_result"
        ),
        "recommendations": state.get(
            "recommendation_result",
            [],
        ),
        "alert": state.get("alert_result"),
        "errors": state.get("errors", []),
    }

    try:
        prompt = f"""
Create the final answer for the user.

Context:
{json.dumps(context, default=str)}

Requirements:
- Answer the question directly.
- Use only supplied evidence.
- Do not invent metrics.
- Mention limitations when data is missing.
- Keep the answer understandable to a business user.
- Include recommendations only when available.
"""

        answer = BedrockChatService().generate(
            prompt=prompt,
            system_prompt=(
                "You are the InsightPilot AI executive "
                "analytics assistant."
            ),
            max_tokens=900,
            temperature=0.1,
        )

        return {
            "final_answer": answer,
            "agents_used": add_agent(
                state,
                "summary_agent",
            ),
        }

    except (
        BedrockChatError,
        RuntimeError,
    ) as exc:
        fallback = (
            base_answer
            or "The requested analysis could not be completed."
        )

        return {
            "final_answer": fallback,
            "errors": add_error(
                state,
                f"Summary Agent: {exc}",
            ),
            "agents_used": add_agent(
                state,
                "summary_agent",
            ),
        }