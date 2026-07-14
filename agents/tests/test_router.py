import pytest

from agents.router import route_question


@pytest.mark.parametrize(
    ("question", "expected_route"),
    [
        ("How is churn calculated?", "rag"),
        ("Show monthly revenue", "sql"),
        ("Predict churn for a customer", "ml"),
        (
            "What is the latest data quality score?",
            "data_quality",
        ),
        (
            "Why did refunds increase?",
            "root_cause",
        ),
        (
            "Create a revenue chart",
            "visualization",
        ),
        (
            "Recommend actions to reduce churn",
            "recommendation",
        ),
    ],
)
def test_router(
    question: str,
    expected_route: str,
) -> None:
    route, _, confidence = route_question(question)

    assert route == expected_route
    assert 0 <= confidence <= 1