from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from backend.app.factory import (
    create_application,
)
from backend.config.settings import (
    get_settings,
)


@pytest.fixture
def app():
    get_settings.cache_clear()

    application = create_application()

    yield application

    application.dependency_overrides.clear()

    get_settings.cache_clear()


@pytest.fixture
def client(app):
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture
def api_headers():
    settings = get_settings()

    return {
        "X-API-Key": settings.api_key,
    }