from __future__ import annotations

import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from data_pipeline.data_generator.config import NUM_REFUNDS
from data_pipeline.data_generator.utils import generate_id


def generate_refunds(
    orders_df: pd.DataFrame,
    output_path: Path,
) -> pd.DataFrame:
    """
    Generate refund records linked to valid orders.

    A small number of intentionally invalid refund amounts are
    included for later data-quality testing.
    """
    refunds: list[dict] = []

    order_records = (
        orders_df[
            [
                "order_id",
                "customer_id",
                "order_date",
                "order_amount",
                "order_status",
            ]
        ]
        .dropna(subset=["order_id"])
        .drop_duplicates(subset=["order_id"])
        .to_dict("records")
    )

    refundable_orders = [
        order
        for order in order_records
        if order["order_status"]
        in ["Completed", "Delivered", "Returned", "Shipped"]
    ]

    selected_orders = random.sample(
        refundable_orders,
        k=min(NUM_REFUNDS, len(refundable_orders)),
    )

    refund_reasons = [
        "Damaged Item",
        "Wrong Product",
        "Late Delivery",
        "Customer Changed Mind",
        "Product Not as Described",
        "Duplicate Charge",
        "Missing Parts",
        "Quality Issue",
    ]

    refund_methods = [
        "Original Payment Method",
        "Store Credit",
        "Gift Card",
        "Bank Transfer",
    ]

    for index, order in enumerate(selected_orders, start=1):
        order_amount = abs(float(order["order_amount"]))

        try:
            order_date = datetime.strptime(
                str(order["order_date"]),
                "%Y-%m-%d",
            )
        except ValueError:
            order_date = datetime.now()

        refund_date = order_date + timedelta(
            days=random.randint(1, 45)
        )

        refund_amount = round(
            order_amount * random.uniform(0.15, 1.0),
            2,
        )

        # Intentionally create a few refunds larger than the order amount.
        if random.random() < 0.01:
            refund_amount = round(
                order_amount * random.uniform(1.05, 1.5),
                2,
            )

        refund = {
            "refund_id": generate_id(
                "REF",
                index,
                width=8,
            ),
            "order_id": order["order_id"],
            "customer_id": order["customer_id"],
            "refund_date": refund_date.strftime(
                "%Y-%m-%d"
            ),
            "refund_amount": refund_amount,
            "refund_reason": random.choice(
                refund_reasons
            ),
            "refund_method": random.choice(
                refund_methods
            ),
            "refund_status": random.choices(
                ["Approved", "Pending", "Rejected"],
                weights=[82, 12, 6],
                k=1,
            )[0],
            "currency": "USD",
        }

        refunds.append(refund)

    dataframe = pd.DataFrame(refunds)

    # Add missing refund reasons intentionally.
    missing_count = max(
        1,
        int(len(dataframe) * 0.01),
    )

    missing_indices = dataframe.sample(
        n=missing_count,
        random_state=42,
    ).index

    dataframe.loc[
        missing_indices,
        "refund_reason",
    ] = None

    # Add a few duplicate refund records.
    duplicate_count = max(
        1,
        int(len(dataframe) * 0.003),
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
        f"Generated refunds dataset: "
        f"{len(dataframe):,} rows -> {output_path}"
    )

    return dataframe