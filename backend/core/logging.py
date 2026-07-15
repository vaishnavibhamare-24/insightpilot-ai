from __future__ import annotations

import json
import logging
import logging.config
from datetime import datetime, timezone
from typing import Any

from backend.config.settings import get_settings

settings = get_settings()


class JsonFormatter(logging.Formatter):
    def format(
        self,
        record: logging.LogRecord,
    ) -> str:
        payload: dict[str, Any] = {
            "timestamp": datetime.now(
                timezone.utc
            ).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        optional_fields = (
            "request_id",
            "method",
            "path",
            "status_code",
            "latency_ms",
            "route",
            "agent_count",
        )

        for field in optional_fields:
            value = getattr(record, field, None)

            if value is not None:
                payload[field] = value

        if record.exc_info:
            payload["exception"] = (
                self.formatException(record.exc_info)
            )

        return json.dumps(
            payload,
            default=str,
        )


def configure_logging() -> None:
    config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "json": {
                "()": JsonFormatter,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "json",
                "level": settings.log_level.upper(),
            },
        },
        "root": {
            "handlers": ["console"],
            "level": settings.log_level.upper(),
        },
        "loggers": {
            "uvicorn": {
                "handlers": ["console"],
                "level": settings.log_level.upper(),
                "propagate": False,
            },
            "uvicorn.error": {
                "handlers": ["console"],
                "level": settings.log_level.upper(),
                "propagate": False,
            },
            "uvicorn.access": {
                "handlers": ["console"],
                "level": settings.log_level.upper(),
                "propagate": False,
            },
        },
    }

    logging.config.dictConfig(config)