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


def root_cause_agent_node(
    state: AgentState,
) -> AgentState:
    try:
        evidence = {
            "sql_result": state.get("sql_result"),
            "quality_result": state.get(
                "quality_result"
            ),
            "ml_result": state.get("ml_result"),
        }

        prompt = f"""
User question:
{state["message"]}

Available evidence:
{json.dumps(evidence, default=str)}

Identify the most likely causes supported by the evidence.

Rules:
- Do not invent causes.
- Clearly distinguish facts from hypotheses.
- State when evidence is insufficient.
- Return a concise explanation.
"""

        explanation = BedrockChatService().generate(
            prompt=prompt,
            system_prompt=(
                "You are a business root-cause analyst."
            ),
            max_tokens=700,
            temperature=0.1,
        )

        return {
            "root_cause_result": {
                "explanation": explanation,
                "evidence": evidence,
            },
            "agents_used": add_agent(
                state,
                "root_cause_agent",
            ),
        }

    except (
        BedrockChatError,
        RuntimeError,
    ) as exc:
        return {
            "errors": add_error(
                state,
                f"Root Cause Agent: {exc}",
            ),
            "agents_used": add_agent(
                state,
                "root_cause_agent",
            ),
        }