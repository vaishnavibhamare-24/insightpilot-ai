from __future__ import annotations

import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from data_pipeline.data_generator.config import (
    NUM_SUPPORT_TICKETS,
    TICKET_PRIORITY,
    TICKET_STATUS,
)
from data_pipeline.data_generator.utils import generate_id


def generate_support_tickets(
    customers_df: pd.DataFrame,
    orders_df: pd.DataFrame,
    output_path: Path,
) -> pd.DataFrame:
    """
    Generate support tickets linked to customers and, when available,
    to orders.
    """
    tickets: list[dict] = []

    customer_ids = (
        customers_df["customer_id"]
        .dropna()
        .drop_duplicates()
        .tolist()
    )

    order_records = (
        orders_df[
            [
                "order_id",
                "customer_id",
                "order_date",
            ]
        ]
        .dropna(subset=["order_id", "customer_id"])
        .drop_duplicates(subset=["order_id"])
        .to_dict("records")
    )

    issue_types = [
        "Delivery Delay",
        "Refund Request",
        "Payment Issue",
        "Damaged Product",
        "Wrong Product",
        "Account Access",
        "Product Information",
        "Order Cancellation",
        "Missing Item",
        "Technical Issue",
    ]

    channels = [
        "Email",
        "Phone",
        "Chat",
        "Web Form",
        "Social Media",
    ]

    order_lookup: dict[str, list[dict]] = {}

    for order in order_records:
        order_lookup.setdefault(
            order["customer_id"],
            [],
        ).append(order)

    ticket_start = datetime(2023, 1, 1)
    ticket_end = datetime(2026, 6, 30)

    for index in range(1, NUM_SUPPORT_TICKETS + 1):
        customer_id = random.choice(customer_ids)
        customer_orders = order_lookup.get(customer_id, [])

        linked_order = (
            random.choice(customer_orders)
            if customer_orders and random.random() < 0.8
            else None
        )

        created_at = ticket_start + timedelta(
            seconds=random.randint(
                0,
                int((ticket_end - ticket_start).total_seconds()),
            )
        )

        status = random.choice(TICKET_STATUS)

        if status in ["Resolved", "Closed"]:
            resolved_at = created_at + timedelta(
                hours=random.randint(1, 240)
            )
        else:
            resolved_at = None

        ticket = {
            "ticket_id": generate_id(
                "TKT",
                index,
                width=8,
            ),
            "customer_id": customer_id,
            "order_id": (
                linked_order["order_id"]
                if linked_order
                else None
            ),
            "created_at": created_at.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "resolved_at": (
                resolved_at.strftime(
                    "%Y-%m-%d %H:%M:%S"
                )
                if resolved_at
                else None
            ),
            "issue_type": random.choice(issue_types),
            "priority": random.choice(TICKET_PRIORITY),
            "status": status,
            "channel": random.choice(channels),
            "customer_satisfaction_score": (
                random.randint(1, 5)
                if status in ["Resolved", "Closed"]
                else None
            ),
            "description": (
                "Customer reported an issue related to "
                f"{random.choice(issue_types).lower()}."
            ),
        }

        tickets.append(ticket)

    dataframe = pd.DataFrame(tickets)

    # Add a small number of missing issue types.
    missing_count = max(
        1,
        int(len(dataframe) * 0.005),
    )

    missing_indices = dataframe.sample(
        n=missing_count,
        random_state=42,
    ).index

    dataframe.loc[
        missing_indices,
        "issue_type",
    ] = None

    # Add duplicate ticket rows intentionally.
    duplicate_count = max(
        1,
        int(len(dataframe) * 0.002),
    )

    duplicate_rows = dataframe.sample(
        n=duplicate_count,
        random_state=7,
    )

    dataframe = pd.concat(
        [dataframe, duplicate_rows],
        ignore_index=True,
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    dataframe.to_csv(
        output_path,
        index=False,
    )

    print(
        f"Generated support tickets dataset: "
        f"{len(dataframe):,} rows -> {output_path}"
    )

    return dataframe