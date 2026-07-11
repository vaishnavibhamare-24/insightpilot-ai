import pytest

from backend.services.athena_service import (
    AthenaService,
    UnsafeQueryError,
)


@pytest.fixture
def service() -> AthenaService:
    return AthenaService()


@pytest.mark.parametrize(
    "query",
    [
        "SELECT * FROM customers LIMIT 10",
        "SELECT COUNT(*) FROM orders;",
        (
            "WITH totals AS ("
            "SELECT customer_id, COUNT(*) AS total "
            "FROM orders GROUP BY customer_id"
            ") SELECT * FROM totals"
        ),
        "EXPLAIN SELECT * FROM products",
    ],
)
def test_allows_read_only_queries(
    service: AthenaService,
    query: str,
) -> None:
    validated = service.validate_query(query)

    assert validated


@pytest.mark.parametrize(
    "query",
    [
        "DROP TABLE customers",
        "DELETE FROM customers",
        "UPDATE customers SET email = 'x'",
        "INSERT INTO customers VALUES ('1')",
        "CREATE TABLE test AS SELECT * FROM customers",
        "TRUNCATE TABLE customers",
        "ALTER TABLE customers ADD COLUMN test varchar",
        "SELECT * FROM customers; DROP TABLE customers",
    ],
)
def test_rejects_unsafe_queries(
    service: AthenaService,
    query: str,
) -> None:
    with pytest.raises(UnsafeQueryError):
        service.validate_query(query)