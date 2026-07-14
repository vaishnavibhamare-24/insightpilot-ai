from __future__ import annotations

from agents.nodes.common import (
    add_agent,
    add_error,
)
from agents.services.sql_generation_service import (
    SQLGenerationService,
)
from agents.state import AgentState
from backend.services.athena_service import (
    AthenaQueryError,
    AthenaService,
    UnsafeQueryError,
)


def sql_agent_node(
    state: AgentState,
) -> AgentState:
    try:
        sql = SQLGenerationService().generate_sql(
            state["message"]
        )

        athena = AthenaService()

        safe_sql = athena.validate_query(sql)

        result = athena.execute_query(
            query=safe_sql,
            timeout_seconds=45,
            max_results=500,
        )

        return {
            "generated_sql": safe_sql,
            "sql_result": result,
            "agents_used": add_agent(
                state,
                "sql_agent",
            ),
        }

    except (
        AthenaQueryError,
        UnsafeQueryError,
        RuntimeError,
        ValueError,
    ) as exc:
        return {
            "errors": add_error(
                state,
                f"SQL Agent: {exc}",
            ),
            "agents_used": add_agent(
                state,
                "sql_agent",
            ),
        }