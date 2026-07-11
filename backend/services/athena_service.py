from __future__ import annotations

import re
import time
from typing import Any

from botocore.exceptions import (
    BotoCoreError,
    ClientError,
    NoCredentialsError,
    ProfileNotFound,
)

from backend.config.settings import get_settings
from backend.services.aws_session import get_aws_session

settings = get_settings()


class AthenaQueryError(RuntimeError):
    """Raised when Athena cannot execute or return a query."""


class UnsafeQueryError(ValueError):
    """Raised when a query is not considered read-only."""


class AthenaService:
    ALLOWED_START_KEYWORDS = {
        "SELECT",
        "WITH",
        "EXPLAIN",
    }

    FORBIDDEN_KEYWORDS = {
        "ALTER",
        "CREATE",
        "DELETE",
        "DROP",
        "GRANT",
        "INSERT",
        "MERGE",
        "MSCK",
        "RENAME",
        "REPAIR",
        "REVOKE",
        "TRUNCATE",
        "UNLOAD",
        "UPDATE",
        "VACUUM",
    }

    def __init__(self) -> None:
        if not settings.glue_database:
            raise RuntimeError(
                "GLUE_DATABASE is not configured."
            )

        if not settings.athena_output_bucket:
            raise RuntimeError(
                "ATHENA_OUTPUT_BUCKET is not configured."
            )

        try:
            session = get_aws_session()
            self.client = session.client("athena")

        except ProfileNotFound as exc:
            raise RuntimeError(
                f"AWS profile '{settings.aws_profile}' "
                "was not found."
            ) from exc

    @property
    def output_location(self) -> str:
        bucket = settings.athena_output_bucket.strip()

        if bucket.startswith("s3://"):
            bucket = bucket.removeprefix("s3://")

        bucket = bucket.rstrip("/")

        return f"s3://{bucket}/query-results/"

    @staticmethod
    def _remove_sql_comments(query: str) -> str:
        """
        Remove basic single-line and block SQL comments before
        validating the statement.
        """
        without_block_comments = re.sub(
            r"/\*.*?\*/",
            " ",
            query,
            flags=re.DOTALL,
        )

        return re.sub(
            r"--[^\n\r]*",
            " ",
            without_block_comments,
        )

    def validate_query(self, query: str) -> str:
        """
        Permit only one read-only SELECT, WITH, or EXPLAIN query.
        """
        cleaned_query = self._remove_sql_comments(
            query
        ).strip()

        if not cleaned_query:
            raise UnsafeQueryError(
                "The query cannot be empty."
            )

        query_without_final_semicolon = (
            cleaned_query[:-1].strip()
            if cleaned_query.endswith(";")
            else cleaned_query
        )

        if ";" in query_without_final_semicolon:
            raise UnsafeQueryError(
                "Only one SQL statement is allowed."
            )

        first_match = re.match(
            r"^\s*([A-Za-z]+)",
            query_without_final_semicolon,
        )

        if first_match is None:
            raise UnsafeQueryError(
                "Unable to determine the SQL statement type."
            )

        first_keyword = first_match.group(1).upper()

        if first_keyword not in self.ALLOWED_START_KEYWORDS:
            raise UnsafeQueryError(
                "Only SELECT, WITH, and EXPLAIN queries "
                "are allowed."
            )

        uppercase_query = (
            query_without_final_semicolon.upper()
        )

        for keyword in self.FORBIDDEN_KEYWORDS:
            if re.search(
                rf"\b{re.escape(keyword)}\b",
                uppercase_query,
            ):
                raise UnsafeQueryError(
                    f"Keyword '{keyword}' is not allowed."
                )

        return query_without_final_semicolon

    def start_query(self, query: str) -> str:
        """
        Submit a query to Athena and return its execution ID.
        """
        safe_query = self.validate_query(query)

        try:
            response = self.client.start_query_execution(
                QueryString=safe_query,
                QueryExecutionContext={
                    "Database": settings.glue_database,
                    "Catalog": "AwsDataCatalog",
                },
                ResultConfiguration={
                    "OutputLocation": self.output_location,
                    "EncryptionConfiguration": {
                        "EncryptionOption": "SSE_S3",
                    },
                },
                WorkGroup="primary",
            )

            return response["QueryExecutionId"]

        except NoCredentialsError as exc:
            raise AthenaQueryError(
                "AWS credentials were not found."
            ) from exc

        except ClientError as exc:
            raise self._client_error(exc) from exc

        except BotoCoreError as exc:
            raise AthenaQueryError(
                "AWS SDK could not communicate with Athena."
            ) from exc

    def wait_for_query(
        self,
        query_execution_id: str,
        timeout_seconds: int,
        poll_interval_seconds: float = 0.75,
    ) -> dict[str, Any]:
        """
        Poll Athena until the query succeeds, fails, is cancelled,
        or reaches the timeout.
        """
        deadline = time.monotonic() + timeout_seconds

        while time.monotonic() < deadline:
            try:
                response = self.client.get_query_execution(
                    QueryExecutionId=query_execution_id,
                )

            except ClientError as exc:
                raise self._client_error(exc) from exc

            except BotoCoreError as exc:
                raise AthenaQueryError(
                    "Unable to check Athena query status."
                ) from exc

            execution = response["QueryExecution"]
            status = execution["Status"]
            state = status["State"]

            if state == "SUCCEEDED":
                return execution

            if state in {"FAILED", "CANCELLED"}:
                reason = status.get(
                    "StateChangeReason",
                    "Athena did not provide a reason.",
                )

                raise AthenaQueryError(
                    f"Athena query {state.lower()}: "
                    f"{reason}"
                )

            time.sleep(poll_interval_seconds)

        self.cancel_query(query_execution_id)

        raise AthenaQueryError(
            f"Athena query exceeded the "
            f"{timeout_seconds}-second timeout "
            "and was cancelled."
        )

    def cancel_query(
        self,
        query_execution_id: str,
    ) -> None:
        """
        Request cancellation of an Athena query.
        """
        try:
            self.client.stop_query_execution(
                QueryExecutionId=query_execution_id,
            )
        except (ClientError, BotoCoreError):
            return

    def get_results(
        self,
        query_execution_id: str,
        max_results: int,
    ) -> tuple[list[str], list[dict[str, Any]]]:
        """
        Retrieve paginated Athena results and convert them into
        dictionaries keyed by column name.
        """
        columns: list[str] = []
        rows: list[dict[str, Any]] = []
        first_page = True

        try:
            paginator = self.client.get_paginator(
                "get_query_results"
            )

            page_iterator = paginator.paginate(
                QueryExecutionId=query_execution_id,
                PaginationConfig={
                    "PageSize": min(max_results + 1, 1000),
                },
            )

            for page in page_iterator:
                result_set = page["ResultSet"]

                if not columns:
                    column_info = result_set[
                        "ResultSetMetadata"
                    ]["ColumnInfo"]

                    columns = [
                        column.get(
                            "Label",
                            column.get("Name", "column"),
                        )
                        for column in column_info
                    ]

                raw_rows = result_set.get("Rows", [])

                if first_page and raw_rows:
                    raw_rows = raw_rows[1:]
                    first_page = False

                for raw_row in raw_rows:
                    values = [
                        cell.get("VarCharValue")
                        for cell in raw_row.get("Data", [])
                    ]

                    if len(values) < len(columns):
                        values.extend(
                            [None]
                            * (len(columns) - len(values))
                        )

                    row = dict(
                        zip(
                            columns,
                            values,
                            strict=False,
                        )
                    )

                    rows.append(row)

                    if len(rows) >= max_results:
                        return columns, rows

            return columns, rows

        except ClientError as exc:
            raise self._client_error(exc) from exc

        except BotoCoreError as exc:
            raise AthenaQueryError(
                "Unable to retrieve Athena results."
            ) from exc

    @staticmethod
    def get_statistics(
        execution: dict[str, Any],
    ) -> dict[str, int | None]:
        statistics = execution.get(
            "Statistics",
            {}
        )

        return {
            "engine_execution_time_ms": (
                statistics.get(
                    "EngineExecutionTimeInMillis"
                )
            ),
            "data_scanned_bytes": statistics.get(
                "DataScannedInBytes"
            ),
            "total_execution_time_ms": statistics.get(
                "TotalExecutionTimeInMillis"
            ),
        }

    def execute_query(
        self,
        query: str,
        timeout_seconds: int = 30,
        max_results: int = 1000,
    ) -> dict[str, Any]:
        """
        Validate, submit, wait for, and retrieve an Athena query.
        """
        query_execution_id = self.start_query(query)

        execution = self.wait_for_query(
            query_execution_id=query_execution_id,
            timeout_seconds=timeout_seconds,
        )

        columns, rows = self.get_results(
            query_execution_id=query_execution_id,
            max_results=max_results,
        )

        return {
            "query_execution_id": query_execution_id,
            "status": execution["Status"]["State"],
            "columns": columns,
            "rows": rows,
            "row_count": len(rows),
            "statistics": self.get_statistics(
                execution
            ),
        }

    @staticmethod
    def _client_error(
        exc: ClientError,
    ) -> AthenaQueryError:
        error = exc.response.get("Error", {})
        code = error.get("Code", "Unknown")
        message = error.get(
            "Message",
            "Athena request failed.",
        )

        return AthenaQueryError(
            f"Athena error {code}: {message}"
        )