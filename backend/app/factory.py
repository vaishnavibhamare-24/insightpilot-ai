from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import (
    CORSMiddleware,
)
from slowapi import (
    _rate_limit_exceeded_handler,
)
from slowapi.errors import RateLimitExceeded

from backend.api.v1.router import api_router
from backend.app.lifespan import lifespan
from backend.config.settings import get_settings
from backend.core.exception_handlers import (
    register_exception_handlers,
)
from backend.core.logging import (
    configure_logging,
)
from backend.core.middleware import (
    RequestContextMiddleware,
)
from backend.core.rate_limit import limiter


settings = get_settings()


def create_application() -> FastAPI:
    configure_logging()

    app = FastAPI(
        title=settings.app_name,
        description=settings.app_description,
        version=settings.app_version,
        debug=settings.debug,
        lifespan=lifespan,
        docs_url=(
            "/docs"
            if settings.app_env != "production"
            else None
        ),
        redoc_url=(
            "/redoc"
            if settings.app_env != "production"
            else None
        ),
        openapi_url=(
            "/openapi.json"
            if settings.app_env != "production"
            else None
        ),
    )

    app.state.limiter = limiter

    app.add_exception_handler(
        RateLimitExceeded,
        _rate_limit_exceeded_handler,
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origin_list,
        allow_credentials=True,
        allow_methods=[
            "GET",
            "POST",
            "PUT",
            "PATCH",
            "DELETE",
            "OPTIONS",
        ],
        allow_headers=[
            "Authorization",
            "Content-Type",
            "X-API-Key",
            "X-Request-ID",
        ],
        expose_headers=[
            "X-Request-ID",
            "X-Process-Time-MS",
        ],
    )

    app.add_middleware(
        RequestContextMiddleware
    )

    register_exception_handlers(app)

    app.include_router(
        api_router,
        prefix=settings.api_v1_prefix,
    )

    return app