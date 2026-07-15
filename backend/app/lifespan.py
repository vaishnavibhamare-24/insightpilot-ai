from __future__ import annotations

import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI

from backend.config.settings import get_settings


logger = logging.getLogger(__name__)
settings = get_settings()


@asynccontextmanager
async def lifespan(
    app: FastAPI,
):
    logger.info(
        "Starting InsightPilot API. "
        "environment=%s version=%s",
        settings.app_env,
        settings.app_version,
    )

    app.state.started = True

    yield

    logger.info(
        "Stopping InsightPilot API."
    )

    app.state.started = False