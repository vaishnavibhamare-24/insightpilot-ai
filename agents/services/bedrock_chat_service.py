from __future__ import annotations

from botocore.exceptions import (
    BotoCoreError,
    ClientError,
)

from backend.config.settings import get_settings
from backend.services.aws_session import get_aws_session


settings = get_settings()


class BedrockChatError(RuntimeError):
    """Raised when direct Bedrock inference fails."""


class BedrockChatService:
    def __init__(self) -> None:
        if not settings.bedrock_chat_model_id:
            raise RuntimeError(
                "BEDROCK_CHAT_MODEL_ID is not configured."
            )

        session = get_aws_session()

        self.client = session.client(
            "bedrock-runtime"
        )

    def generate(
        self,
        prompt: str,
        system_prompt: str | None = None,
        max_tokens: int = 1000,
        temperature: float = 0.1,
    ) -> str:
        request: dict = {
            "modelId": settings.bedrock_chat_model_id,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "text": prompt,
                        }
                    ],
                }
            ],
            "inferenceConfig": {
                "maxTokens": max_tokens,
                "temperature": temperature,
                "topP": 0.9,
            },
        }

        if system_prompt:
            request["system"] = [
                {
                    "text": system_prompt,
                }
            ]

        try:
            response = self.client.converse(
                **request
            )

            content = (
                response["output"]
                ["message"]
                ["content"]
            )

            text_parts = [
                item["text"]
                for item in content
                if "text" in item
            ]

            return "\n".join(
                text_parts
            ).strip()

        except ClientError as exc:
            error = exc.response.get(
                "Error",
                {},
            )

            raise BedrockChatError(
                "Bedrock error "
                f"{error.get('Code', 'Unknown')}: "
                f"{error.get('Message', 'Request failed.')}"
            ) from exc

        except BotoCoreError as exc:
            raise BedrockChatError(
                "Unable to communicate with Bedrock."
            ) from exc