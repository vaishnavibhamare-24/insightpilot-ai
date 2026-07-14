from __future__ import annotations

from agents.nodes.common import add_agent
from agents.state import AgentState


def visualization_agent_node(
    state: AgentState,
) -> AgentState:
    sql_result = state.get("sql_result") or {}

    columns = sql_result.get("columns", [])
    rows = sql_result.get("rows", [])

    chart_type = "table"
    x_field = None
    y_field = None

    if len(columns) >= 2 and rows:
        first_column = columns[0].lower()

        if any(
            term in first_column
            for term in (
                "month",
                "date",
                "year",
                "time",
            )
        ):
            chart_type = "line"
        else:
            chart_type = "bar"

        x_field = columns[0]
        y_field = columns[1]

    return {
        "visualization": {
            "chart_type": chart_type,
            "x_field": x_field,
            "y_field": y_field,
            "title": state["message"],
            "data": rows,
        },
        "agents_used": add_agent(
            state,
            "visualization_agent",
        ),
    }