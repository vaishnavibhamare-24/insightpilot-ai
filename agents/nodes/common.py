from __future__ import annotations

from typing import Any

from agents.state import AgentState


def add_agent(
    state: AgentState,
    agent_name: str,
) -> list[str]:
    agents = list(state.get("agents_used", []))

    if agent_name not in agents:
        agents.append(agent_name)

    return agents


def add_error(
    state: AgentState,
    message: str,
) -> list[str]:
    errors = list(state.get("errors", []))
    errors.append(message)

    return errors


def safe_result(
    value: Any,
) -> dict[str, Any]:
    if isinstance(value, dict):
        return value

    return {
        "value": value,
    }