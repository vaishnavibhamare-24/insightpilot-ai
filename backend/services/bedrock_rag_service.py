from __future__ import annotations

from pathlib import PurePosixPath
from typing import Any

from botocore.exceptions import BotoCoreError, ClientError

from backend.config.settings import get_settings
from backend.services.aws_session import get_aws_session
import logging
import time


settings = get_settings()


class BedrockRAGError(RuntimeError):
    """Raised when the Bedrock RAG operation fails."""


class BedrockRAGService:
    def __init__(self) -> None:
        if not settings.bedrock_knowledge_base_id:
            raise RuntimeError(
                "BEDROCK_KNOWLEDGE_BASE_ID is not configured."
            )

        if not settings.bedrock_model_arn:
            raise RuntimeError(
                "BEDROCK_MODEL_ARN is not configured."
            )

        session = get_aws_session()

        self.client = session.client(
            "bedrock-agent-runtime"
        )

    def query(
        self,
        question: str,
        session_id: str | None = None,
    ) -> dict[str, Any]:
        cleaned_question = question.strip()

        if not cleaned_question:
            raise ValueError("Question must not be empty.")

        request: dict[str, Any] = {
            "input": {
                "text": cleaned_question,
            },
            "retrieveAndGenerateConfiguration": {
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseConfiguration": {
                    "knowledgeBaseId": (
                        settings.bedrock_knowledge_base_id
                    ),
                    "modelArn": settings.bedrock_model_arn,
                    "retrievalConfiguration": {
                        "vectorSearchConfiguration": {
                            "numberOfResults": (
                                settings
                                .bedrock_rag_number_of_results
                            )
                        }
                    },
                    "generationConfiguration": {
                        "promptTemplate": {
                            "textPromptTemplate": (
                                "You are the InsightPilot AI business "
                                "assistant. Answer only from the retrieved "
                                "business documentation. If the retrieved "
                                "information is insufficient, clearly say "
                                "that the answer is not available in the "
                                "current knowledge base.\n\n"
                                "$search_results$\n\n"
                                "$output_format_instructions$\n\n"
                                "Question: $query$\n"
                                "Answer:"
                            )
                        }
                    },
                },
            },
        }

        if session_id:
            request["sessionId"] = session_id

        try:
            response = self.client.retrieve_and_generate(
                **request
            )

            answer = (
                response
                .get("output", {})
                .get("text", "")
            )

            citations = self._extract_citations(
                response.get("citations", [])
            )

            return {
                "answer": answer,
                "citations": citations,
                "session_id": response.get("sessionId"),
            }

        except ClientError as exc:
            error = exc.response.get("Error", {})

            raise BedrockRAGError(
                "Bedrock error "
                f"{error.get('Code', 'Unknown')}: "
                f"{error.get('Message', 'Request failed.')}"
            ) from exc

        except BotoCoreError as exc:
            raise BedrockRAGError(
                "Unable to communicate with Amazon Bedrock."
            ) from exc

    @staticmethod
    def _extract_citations(
        raw_citations: list[dict[str, Any]],
    ) -> list[dict[str, str | None]]:
        citations: list[dict[str, str | None]] = []
        seen_sources: set[str] = set()

        for citation in raw_citations:
            generated_part = citation.get(
                "generatedResponsePart",
                {},
            )

            cited_text = (
                generated_part
                .get("textResponsePart", {})
                .get("text")
            )

            retrieved_references = citation.get(
                "retrievedReferences",
                [],
            )

            for reference in retrieved_references:
                location = reference.get(
                    "location",
                    {},
                )

                source_uri = (
                    location
                    .get("s3Location", {})
                    .get("uri")
                )

                if not source_uri:
                    source_uri = (
                        location
                        .get("webLocation", {})
                        .get("url")
                    )

                if not source_uri:
                    source_uri = (
                        location
                        .get("customDocumentLocation", {})
                        .get("id")
                    )

                deduplication_key = (
                    source_uri or repr(reference)
                )

                if deduplication_key in seen_sources:
                    continue

                seen_sources.add(deduplication_key)

                document_name: str | None = None

                if source_uri:
                    document_name = PurePosixPath(
                        source_uri
                    ).name

                content_text = (
                    reference
                    .get("content", {})
                    .get("text")
                )

                citations.append(
                    {
                        "text": content_text or cited_text,
                        "source_uri": source_uri,
                        "document_name": document_name,
                    }
                )

        return citations