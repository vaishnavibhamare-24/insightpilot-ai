from __future__ import annotations

from agents.state import AgentRoute, AgentState


ROUTING_RULES: list[
    tuple[AgentRoute, tuple[str, ...]]
] = [
    (
        "root_cause",
        (
            "why did",
            "why has",
            "root cause",
            "reason for",
            "explain the decrease",
            "explain the increase",
        ),
    ),
    (
        "data_quality",
        (
            "data quality",
            "quality score",
            "failed rules",
            "invalid records",
            "missing values",
            "pipeline quality",
        ),
    ),
    (
        "ml",
        (
            "predict churn",
            "churn probability",
            "churn risk",
            "forecast revenue",
            "revenue forecast",
            "prediction",
        ),
    ),
    (
        "rag",
        (
            "how is",
            "what is the definition",
            "policy",
            "business rule",
            "explain the model",
            "what does",
            "definition of",
        ),
    ),
    (
        "visualization",
        (
            "chart",
            "graph",
            "plot",
            "visualize",
            "trend chart",
        ),
    ),
    (
        "alert",
        (
            "alert",
            "warning",
            "notify",
            "threshold",
            "critical",
        ),
    ),
    (
        "recommendation",
        (
            "recommend",
            "what should we do",
            "suggest actions",
            "next steps",
        ),
    ),
    (
        "sql",
        (
            "show",
            "list",
            "count",
            "total",
            "average",
            "top",
            "monthly",
            "revenue",
            "orders",
            "refunds",
            "customers",
            "tickets",
        ),
    ),
]


def route_question(
    message: str,
) -> tuple[AgentRoute, str, float]:
    normalized = " ".join(
        message.lower().split()
    )

    for route, keywords in ROUTING_RULES:
        matched = [
            keyword
            for keyword in keywords
            if keyword in normalized
        ]

        if matched:
            return (
                route,
                (
                    "Matched routing keywords: "
                    f"{', '.join(matched)}"
                ),
                min(
                    0.95,
                    0.65 + 0.05 * len(matched),
                ),
            )

    return (
        "general",
        "No specialized routing rule matched.",
        0.50,
    )


def router_node(
    state: AgentState,
) -> AgentState:
    route, reason, confidence = route_question(
        state["message"]
    )

    agents_used = list(
        state.get("agents_used", [])
    )

    if "router_agent" not in agents_used:
        agents_used.append("router_agent")

    return {
        "route": route,
        "requested_route": route,
        "route_reason": reason,
        "confidence": confidence,
        "agents_used": agents_used,
    }