from backend.services.bedrock_rag_service import (
    BedrockRAGService,
)


def test_churn_definition_query() -> None:
    result = BedrockRAGService().query(
        "Which features are used by the churn model?"
    )

    assert result["answer"]
    assert isinstance(result["citations"], list)

    source_names = {
        citation.get("document_name")
        for citation in result["citations"]
    }

    assert "churn_model_guide.md" in source_names
