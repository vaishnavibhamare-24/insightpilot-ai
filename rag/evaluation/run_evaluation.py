from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from backend.services.bedrock_rag_service import BedrockRAGService


BASE_DIR = Path(__file__).resolve().parent
DATASET_PATH = BASE_DIR / "evaluation_dataset.json"
RESULTS_DIR = BASE_DIR / "results"
RESULTS_PATH = RESULTS_DIR / "rag_evaluation.json"


def load_dataset() -> list[dict[str, str]]:
    with DATASET_PATH.open(
        "r",
        encoding="utf-8",
    ) as file:
        data = json.load(file)

    if not isinstance(data, list):
        raise ValueError(
            "The evaluation dataset must contain a JSON list."
        )

    return data


def normalize_text(text: str) -> str:
    normalized = text.lower()

    normalized = re.sub(
        r"[^a-z0-9.\s]",
        " ",
        normalized,
    )

    normalized = re.sub(
        r"\s+",
        " ",
        normalized,
    )

    return normalized.strip()


def extract_keywords(text: str) -> set[str]:
    stop_words = {
        "a",
        "an",
        "and",
        "are",
        "as",
        "at",
        "be",
        "because",
        "by",
        "for",
        "from",
        "in",
        "is",
        "it",
        "of",
        "on",
        "or",
        "so",
        "that",
        "the",
        "their",
        "to",
        "used",
        "uses",
        "when",
        "with",
    }

    words = normalize_text(text).split()

    return {
        word
        for word in words
        if word not in stop_words and len(word) > 1
    }


def calculate_keyword_recall(
    generated_answer: str,
    reference_answer: str,
) -> float:
    reference_keywords = extract_keywords(
        reference_answer
    )

    if not reference_keywords:
        return 1.0

    generated_keywords = extract_keywords(
        generated_answer
    )

    matched_keywords = (
        reference_keywords & generated_keywords
    )

    return len(matched_keywords) / len(
        reference_keywords
    )


def get_source_names(
    citations: list[dict[str, Any]],
) -> set[str]:
    return {
        str(citation.get("document_name"))
        for citation in citations
        if citation.get("document_name")
    }


def run_evaluation() -> dict[str, Any]:
    dataset = load_dataset()
    service = BedrockRAGService()

    evaluation_rows: list[dict[str, Any]] = []

    source_matches = 0
    keyword_recall_scores: list[float] = []

    for index, item in enumerate(dataset, start=1):
        question = item["question"]
        reference_answer = item["reference_answer"]
        expected_source = item["expected_source"]

        print(
            f"Evaluating question {index}/{len(dataset)}: "
            f"{question}"
        )

        result = service.query(question)

        answer = result.get("answer", "")
        citations = result.get("citations", [])

        retrieved_sources = get_source_names(
            citations
        )

        source_match = (
            expected_source in retrieved_sources
        )

        if source_match:
            source_matches += 1

        keyword_recall = calculate_keyword_recall(
            generated_answer=answer,
            reference_answer=reference_answer,
        )

        keyword_recall_scores.append(
            keyword_recall
        )

        evaluation_rows.append(
            {
                "question": question,
                "reference_answer": reference_answer,
                "generated_answer": answer,
                "expected_source": expected_source,
                "retrieved_sources": sorted(
                    retrieved_sources
                ),
                "source_match": source_match,
                "answer_keyword_recall": round(
                    keyword_recall,
                    4,
                ),
                "session_id": result.get(
                    "session_id"
                ),
            }
        )

    total_questions = len(dataset)

    source_retrieval_accuracy = (
        source_matches / total_questions
        if total_questions
        else 0.0
    )

    average_answer_keyword_recall = (
        sum(keyword_recall_scores)
        / len(keyword_recall_scores)
        if keyword_recall_scores
        else 0.0
    )

    summary = {
        "total_questions": total_questions,
        "source_retrieval_accuracy": round(
            source_retrieval_accuracy,
            4,
        ),
        "average_answer_keyword_recall": round(
            average_answer_keyword_recall,
            4,
        ),
        "results": evaluation_rows,
    }

    RESULTS_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    with RESULTS_PATH.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            summary,
            file,
            indent=2,
            ensure_ascii=False,
        )

    return summary


def main() -> None:
    summary = run_evaluation()

    print("\nRAG evaluation complete")
    print(
        "total_questions:",
        summary["total_questions"],
    )
    print(
        "source_retrieval_accuracy:",
        summary["source_retrieval_accuracy"],
    )
    print(
        "average_answer_keyword_recall:",
        summary[
            "average_answer_keyword_recall"
        ],
    )
    print(
        "results_file:",
        RESULTS_PATH,
    )


if __name__ == "__main__":
    main()