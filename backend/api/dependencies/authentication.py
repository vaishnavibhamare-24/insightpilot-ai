from __future__ import annotations

import secrets

from fastapi import Security
from fastapi.security import APIKeyHeader

from backend.config.settings import get_settings
from backend.core.exceptions import (
    AuthenticationError,
)

settings = get_settings()

api_key_header = APIKeyHeader(
    name="X-API-Key",
    auto_error=False,
)


def verify_api_key(
    supplied_api_key: str | None = Security(
        api_key_header
    ),
) -> str:
    if not settings.api_key_enabled:
        return "authentication-disabled"

    if not settings.api_key:
        raise AuthenticationError(
            "The server API key is not configured."
        )

    if not supplied_api_key:
        raise AuthenticationError(
            "The X-API-Key header is required."
        )

    if not secrets.compare_digest(
        supplied_api_key,
        settings.api_key,
    ):
        raise AuthenticationError(
            "The supplied API key is invalid."
        )

    return supplied_api_key