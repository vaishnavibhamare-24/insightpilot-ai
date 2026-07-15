from __future__ import annotations

import pytest

from backend.api.dependencies.authentication import (
    verify_api_key,
)
from backend.config.settings import get_settings
from backend.core.exceptions import (
    AuthenticationError,
)


def test_missing_api_key() -> None:
    with pytest.raises(
        AuthenticationError
    ) as exc_info:
        verify_api_key(None)

    assert exc_info.value.status_code == 401
    assert (
        exc_info.value.error_code
        == "AUTHENTICATION_FAILED"
    )


def test_invalid_api_key() -> None:
    with pytest.raises(
        AuthenticationError
    ) as exc_info:
        verify_api_key(
            "incorrect-key"
        )

    assert exc_info.value.status_code == 401
    assert (
        exc_info.value.error_code
        == "AUTHENTICATION_FAILED"
    )


def test_valid_api_key() -> None:
    settings = get_settings()

    result = verify_api_key(
        settings.api_key
    )

    assert result == settings.api_key