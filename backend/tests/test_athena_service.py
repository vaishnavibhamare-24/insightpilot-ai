from backend.services.athena_service import (
    AthenaService,
)


def test_customer_count_query() -> None:
    result = AthenaService().execute_query(
        query=(
            "SELECT COUNT(*) AS total "
            "FROM customers"
        ),
        timeout_seconds=30,
        max_results=10,
    )

    assert result["status"] == "SUCCEEDED"
    assert result["columns"] == ["total"]
    assert result["row_count"] == 1

    total = int(result["rows"][0]["total"])

    assert total > 0