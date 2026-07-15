from __future__ import annotations

from typing import Any


class InsightPilotError(Exception):
    status_code = 500
    error_code = "INSIGHTPILOT_ERROR"
    default_message = "An application error occurred."

    def __init__(
        self,
        message: str | None = None,
        *,
        details: Any | None = None,
    ) -> None:
        self.message = message or self.default_message
        self.details = details

        super().__init__(self.message)


class ResourceNotFoundError(InsightPilotError):
    status_code = 404
    error_code = "RESOURCE_NOT_FOUND"
    default_message = "The requested resource was not found."


class AuthenticationError(InsightPilotError):
    status_code = 401
    error_code = "AUTHENTICATION_FAILED"
    default_message = "Authentication failed."


class AuthorizationError(InsightPilotError):
    status_code = 403
    error_code = "AUTHORIZATION_FAILED"
    default_message = (
        "You are not allowed to perform this operation."
    )


class ValidationError(InsightPilotError):
    status_code = 400
    error_code = "VALIDATION_ERROR"
    default_message = "The request is invalid."


class ExternalServiceError(InsightPilotError):
    status_code = 503
    error_code = "EXTERNAL_SERVICE_ERROR"
    default_message = "An external service is unavailable."


class QueryExecutionError(ExternalServiceError):
    error_code = "QUERY_EXECUTION_FAILED"
    default_message = (
        "The analytics query could not be completed."
    )


class AgentExecutionError(ExternalServiceError):
    error_code = "AGENT_EXECUTION_FAILED"
    default_message = (
        "The agent workflow could not be completed."
    )