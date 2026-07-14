from __future__ import annotations

import logging
import time
import uuid
from typing import Any

from agents.graph import agent_graph


logger = logging.getLogger(__name__)


class AgentService:
    def run(
        self,
        message: str,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        effective_session_id = (
            session_id or str(uuid.uuid4())
        )

        started_at = time.perf_counter()

        initial_state = {
            "message": message.strip(),
            "session_id": effective_session_id,
            "agents_used": [],
            "citations": [],
            "recommendation_result": [],
            "errors": [],
        }

        result = agent_graph.invoke(
            initial_state,
            config={
                "recursion_limit": 12,
            },
        )

        latency_ms = (
            time.perf_counter() - started_at
        ) * 1000

        logger.info(
            "Agent workflow completed. "
            "route=%s agents=%s latency_ms=%.2f errors=%s",
            result.get("route"),
            result.get("agents_used"),
            latency_ms,
            len(result.get("errors", [])),
        )

        return {
            "answer": result.get(
                "final_answer",
                "No answer was generated.",
            ),
            "route": result.get("route"),
            "route_reason": result.get(
                "route_reason"
            ),
            "confidence": result.get(
                "confidence"
            ),
            "agents_used": result.get(
                "agents_used",
                [],
            ),
            "generated_sql": result.get(
                "generated_sql"
            ),
            "data": result.get("sql_result"),
            "citations": result.get(
                "citations",
                [],
            ),
            "visualization": result.get(
                "visualization"
            ),
            "recommendations": result.get(
                "recommendation_result",
                [],
            ),
            "alert": result.get(
                "alert_result"
            ),
            "errors": result.get(
                "errors",
                [],
            ),
            "session_id": result.get(
                "session_id",
                effective_session_id,
            ),
            "latency_ms": round(
                latency_ms,
                2,
            ),
        }