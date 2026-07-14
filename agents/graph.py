from __future__ import annotations

from typing import Literal

from langgraph.graph import (
    END,
    START,
    StateGraph,
)

from agents.nodes.alert_agent import (
    alert_agent_node,
)
from agents.nodes.data_quality_agent import (
    data_quality_agent_node,
)
from agents.nodes.ml_agent import (
    ml_agent_node,
)
from agents.nodes.rag_agent import (
    rag_agent_node,
)
from agents.nodes.recommendation_agent import (
    recommendation_agent_node,
)
from agents.nodes.root_cause_agent import (
    root_cause_agent_node,
)
from agents.nodes.sql_agent import (
    sql_agent_node,
)
from agents.nodes.summary_agent import (
    summary_agent_node,
)
from agents.nodes.visualization_agent import (
    visualization_agent_node,
)
from agents.router import router_node
from agents.state import AgentState


RouteName = Literal[
    "sql",
    "rag",
    "ml",
    "data_quality",
    "visualization",
    "root_cause",
    "recommendation",
    "alert",
    "general",
]


def route_from_state(
    state: AgentState,
) -> RouteName:
    return state.get("route", "general")


def after_sql(
    state: AgentState,
) -> str:
    requested = state.get(
        "requested_route",
        state.get("route"),
    )

    if requested == "visualization":
        return "visualization"

    if requested == "root_cause":
        return "root_cause"

    if requested == "recommendation":
        return "recommendation"

    return "summary"


def after_quality(
    state: AgentState,
) -> str:
    if state.get("requested_route") == "alert":
        return "alert"

    return "summary"


def general_node(
    state: AgentState,
) -> AgentState:
    agents_used = list(
        state.get("agents_used", [])
    )

    if "general_agent" not in agents_used:
        agents_used.append("general_agent")

    return {
        "final_answer": (
            "I can help with analytics, business rules, "
            "churn prediction, revenue forecasting, "
            "data quality, visualizations, and alerts. "
            "Please ask a more specific question."
        ),
        "agents_used": agents_used,
    }


def build_agent_graph():
    builder = StateGraph(AgentState)

    builder.add_node(
        "router",
        router_node,
    )
    builder.add_node(
        "sql",
        sql_agent_node,
    )
    builder.add_node(
        "rag",
        rag_agent_node,
    )
    builder.add_node(
        "ml",
        ml_agent_node,
    )
    builder.add_node(
        "data_quality",
        data_quality_agent_node,
    )
    builder.add_node(
        "visualization",
        visualization_agent_node,
    )
    builder.add_node(
        "root_cause",
        root_cause_agent_node,
    )
    builder.add_node(
        "recommendation",
        recommendation_agent_node,
    )
    builder.add_node(
        "alert",
        alert_agent_node,
    )
    builder.add_node(
        "summary",
        summary_agent_node,
    )
    builder.add_node(
        "general",
        general_node,
    )

    builder.add_edge(
        START,
        "router",
    )

    builder.add_conditional_edges(
        "router",
        route_from_state,
        {
            "sql": "sql",
            "rag": "rag",
            "ml": "ml",
            "data_quality": "data_quality",
            "visualization": "sql",
            "root_cause": "sql",
            "recommendation": "sql",
            "alert": "data_quality",
            "general": "general",
        },
    )

    builder.add_conditional_edges(
        "sql",
        after_sql,
        {
            "visualization": "visualization",
            "root_cause": "root_cause",
            "recommendation": "recommendation",
            "summary": "summary",
        },
    )

    builder.add_conditional_edges(
        "data_quality",
        after_quality,
        {
            "alert": "alert",
            "summary": "summary",
        },
    )

    builder.add_edge(
        "rag",
        "summary",
    )
    builder.add_edge(
        "ml",
        "summary",
    )
    builder.add_edge(
        "visualization",
        "summary",
    )
    builder.add_edge(
        "root_cause",
        "recommendation",
    )
    builder.add_edge(
        "recommendation",
        "summary",
    )
    builder.add_edge(
        "alert",
        "summary",
    )

    builder.add_edge(
        "summary",
        END,
    )
    builder.add_edge(
        "general",
        END,
    )

    return builder.compile()


agent_graph = build_agent_graph()