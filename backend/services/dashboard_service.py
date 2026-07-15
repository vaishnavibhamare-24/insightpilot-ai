from __future__ import annotations

from backend.services.athena_service import (
    AthenaService,
)


class DashboardService:
    QUERY = """
    SELECT
        COUNT(DISTINCT order_id) AS total_orders,
        ROUND(SUM(order_amount), 2) AS total_revenue,
        ROUND(AVG(order_amount), 2) AS average_order_value,
        COUNT(DISTINCT customer_id) AS active_customers
    FROM fact_orders
    WHERE order_amount > 0
    """

    def get_metrics(self) -> dict:
        result = AthenaService().execute_query(
            query=self.QUERY,
            timeout_seconds=30,
            max_results=10,
        )

        row = (
            result["rows"][0]
            if result["rows"]
            else {}
        )

        return {
            "kpis": [
                {
                    "name": "Total Orders",
                    "value": int(
                        row.get(
                            "total_orders",
                            0,
                        )
                        or 0
                    ),
                    "unit": "orders",
                },
                {
                    "name": "Total Revenue",
                    "value": float(
                        row.get(
                            "total_revenue",
                            0,
                        )
                        or 0
                    ),
                    "unit": "USD",
                },
                {
                    "name": "Average Order Value",
                    "value": float(
                        row.get(
                            "average_order_value",
                            0,
                        )
                        or 0
                    ),
                    "unit": "USD",
                },
                {
                    "name": "Active Customers",
                    "value": int(
                        row.get(
                            "active_customers",
                            0,
                        )
                        or 0
                    ),
                    "unit": "customers",
                },
            ],
            "source": "Amazon Athena",
        }