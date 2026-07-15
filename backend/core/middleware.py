from __future__ import annotations

import logging
import time
import uuid
from collections.abc import Callable
from typing import Awaitable

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

logger = logging.getLogger(__name__)


class RequestContextMiddleware(
    BaseHTTPMiddleware
):
    async def dispatch(
        self,
        request: Request,
        call_next: Callable[
            [Request],
            Awaitable[Response],
        ],
    ) -> Response:
        incoming_request_id = request.headers.get(
            "X-Request-ID"
        )

        request_id = (
            incoming_request_id
            or str(uuid.uuid4())
        )

        request.state.request_id = request_id

        started_at = time.perf_counter()

        try:
            response = await call_next(request)

        except Exception:
            latency_ms = (
                time.perf_counter() - started_at
            ) * 1000

            logger.exception(
                "Unhandled request failure.",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "path": request.url.path,
                    "latency_ms": round(
                        latency_ms,
                        2,
                    ),
                },
            )

            raise

        latency_ms = (
            time.perf_counter() - started_at
        ) * 1000

        response.headers[
            "X-Request-ID"
        ] = request_id

        response.headers[
            "X-Process-Time-MS"
        ] = f"{latency_ms:.2f}"

        logger.info(
            "HTTP request completed.",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.url.path,
                "status_code": response.status_code,
                "latency_ms": round(
                    latency_ms,
                    2,
                ),
            },
        )

        return response