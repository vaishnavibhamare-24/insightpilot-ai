from __future__ import annotations

from slowapi import Limiter
from slowapi.util import get_remote_address

from backend.config.settings import get_settings


settings = get_settings()


limiter = Limiter(
    key_func=get_remote_address,
    default_limits=[
        settings.rate_limit_default,
    ],
    enabled=settings.rate_limit_enabled,
)