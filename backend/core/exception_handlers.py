from __future__ import annotations

import logging
from typing import Any

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from starlette.exceptions import (
    HTTPException as StarletteHTTPException,
)

from backend.core.exceptions import (
    InsightPilotError,
)

logger = logging.getLogger(__name__)


def request_id_from(
    request: Request,
) -> str | None:
    return getattr(
        request.state,
        "request_id",
        None,
    )


def error_payload(
    *,
    code: str,
    message: str,
    request: Request,
    details: Any | None = None,
) -> dict[str, Any]:
    return {
        "success": False,
        "error": {
            "code": code,
            "message": message,
            "details": details,
        },
        "request_id": request_id_from(
            request
        ),
    }


async def insightpilot_error_handler(
    request: Request,
    exc: InsightPilotError,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=error_payload(
            code=exc.error_code,
            message=exc.message,
            details=exc.details,
            request=request,
        ),
    )


async def validation_error_handler(
    request: Request,
    exc: RequestValidationError,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content=error_payload(
            code="REQUEST_VALIDATION_ERROR",
            message=(
                "The request did not match the "
                "required schema."
            ),
            details=exc.errors(),
            request=request,
        ),
    )


async def http_error_handler(
    request: Request,
    exc: StarletteHTTPException,
) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content=error_payload(
            code="HTTP_ERROR",
            message=str(exc.detail),
            request=request,
        ),
    )


async def unhandled_error_handler(
    request: Request,
    exc: Exception,
) -> JSONResponse:
    logger.exception(
        "Unhandled application exception.",
        extra={
            "request_id": request_id_from(
                request
            ),
            "method": request.method,
            "path": request.url.path,
        },
    )

    return JSONResponse(
        status_code=500,
        content=error_payload(
            code="INTERNAL_SERVER_ERROR",
            message=(
                "An unexpected internal error "
                "occurred."
            ),
            request=request,
        ),
    )


def register_exception_handlers(
    app: FastAPI,
) -> None:
    app.add_exception_handler(
        InsightPilotError,
        insightpilot_error_handler,
    )

    app.add_exception_handler(
        RequestValidationError,
        validation_error_handler,
    )

    app.add_exception_handler(
        StarletteHTTPException,
        http_error_handler,
    )

    app.add_exception_handler(
        Exception,
        unhandled_error_handler,
    )