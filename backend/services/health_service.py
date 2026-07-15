from __future__ import annotations

import time
from collections.abc import Callable

from backend.config.settings import get_settings
from backend.services.aws_session import (
    get_aws_session,
)


settings = get_settings()


class HealthService:
    def _check(
        self,
        name: str,
        function: Callable[[], None],
    ) -> dict:
        started_at = time.perf_counter()

        try:
            function()

            latency_ms = (
                time.perf_counter() - started_at
            ) * 1000

            return {
                "name": name,
                "status": "healthy",
                "latency_ms": round(
                    latency_ms,
                    2,
                ),
                "detail": None,
            }

        except Exception as exc:
            latency_ms = (
                time.perf_counter() - started_at
            ) * 1000

            return {
                "name": name,
                "status": "unhealthy",
                "latency_ms": round(
                    latency_ms,
                    2,
                ),
                "detail": str(exc),
            }

    def check_aws_identity(self) -> None:
        session = get_aws_session()
        client = session.client("sts")

        client.get_caller_identity()

    def check_s3(self) -> None:
        session = get_aws_session()
        client = session.client("s3")

        client.head_bucket(
            Bucket=settings.s3_raw_bucket
        )

    def readiness(self) -> dict:
        dependencies = [
            self._check(
                "aws_sts",
                self.check_aws_identity,
            ),
            self._check(
                "s3_raw_bucket",
                self.check_s3,
            ),
        ]

        healthy = all(
            item["status"] == "healthy"
            for item in dependencies
        )

        return {
            "status": (
                "ready"
                if healthy
                else "not_ready"
            ),
            "dependencies": dependencies,
        }