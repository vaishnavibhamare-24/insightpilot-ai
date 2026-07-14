from __future__ import annotations

import re

from agents.services.bedrock_chat_service import (
    BedrockChatService,
)


SCHEMA_CONTEXT = """
Available Athena tables:

dim_customers:
customer_id, customer_segment, region, total_orders,
lifetime_revenue, average_order_value, churn_label

dim_products:
product_id, product_name, category, brand

fact_orders:
order_id, customer_id, product_id, order_date,
order_amount, quantity, order_status, sales_channel

fact_refunds:
refund_id, order_id, customer_id, refund_date,
refund_amount, refund_status

fact_support_tickets:
ticket_id, customer_id, created_at, resolved_at,
issue_type, priority, status

customer_features:
customer_id, days_since_last_order, total_spend,
number_of_orders, average_order_value, refund_count,
support_ticket_count, website_visits, churn_label

revenue_features:
revenue_month, monthly_orders, monthly_customers,
gross_revenue, average_order_value, units_sold
"""


class SQLGenerationService:
    def __init__(self) -> None:
        self.chat = BedrockChatService()

    def generate_sql(
        self,
        question: str,
    ) -> str:
        prompt = f"""
{SCHEMA_CONTEXT}

Convert the business question below into one Amazon Athena
read-only SQL query.

Rules:
- Return SQL only.
- Do not return Markdown fences.
- Use only the listed tables and columns.
- Use SELECT or WITH only.
- Never use INSERT, UPDATE, DELETE, DROP, ALTER,
  CREATE, UNLOAD, CTAS, or multiple statements.
- Add LIMIT 100 unless the query is an aggregate.
- Prefer processed fact, dimension, and feature tables.

Question:
{question}
"""

        result = self.chat.generate(
            prompt=prompt,
            system_prompt=(
                "You generate safe, read-only Amazon Athena SQL."
            ),
            max_tokens=600,
            temperature=0.0,
        )

        return self._clean_sql(result)

    @staticmethod
    def _clean_sql(
        value: str,
    ) -> str:
        cleaned = value.strip()

        cleaned = re.sub(
            r"^```(?:sql)?",
            "",
            cleaned,
            flags=re.IGNORECASE,
        )

        cleaned = re.sub(
            r"```$",
            "",
            cleaned,
        )

        return cleaned.strip()