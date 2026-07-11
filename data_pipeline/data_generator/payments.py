from __future__ import annotations

import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from data_pipeline.data_generator.config import (
    NUM_PAYMENTS,
    PAYMENT_METHODS,
)
from data_pipeline.data_generator.utils import generate_id


def generate_payments(
    orders_df: pd.DataFrame,
    output_path: Path,
) -> pd.DataFrame:
    """
    Generate payment records linked to orders.

    A small amount of intentionally invalid data is included
    for later ETL and data-quality testing.
    """
    payments: list[dict] = []

    order_records = (
        orders_df[
            [
                "order_id",
                "order_date",
                "order_amount",
                "order_status",
            ]
        ]
        .drop_duplicates(subset=["order_id"])
        .to_dict("records")
    )

    selected_orders = random.sample(
        order_records,
        k=min(NUM_PAYMENTS, len(order_records)),
    )

    for index, order in enumerate(selected_orders, start=1):
        order_amount = abs(float(order["order_amount"]))

        try:
            order_date = datetime.strptime(
                str(order["order_date"]),
                "%Y-%m-%d",
            )
        except ValueError:
            order_date = datetime.now()

        payment_date = order_date + timedelta(
            days=random.randint(0, 3),
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
        )

        if order["order_status"] == "Cancelled":
            payment_status = random.choice(
                ["Failed", "Cancelled", "Refunded"]
            )
        else:
            payment_status = random.choices(
                ["Completed", "Pending", "Failed", "Refunded"],
                weights=[85, 7, 5, 3],
                k=1,
            )[0]

        payment_amount = order_amount

        # Add a small number of negative payment amounts intentionally.
        if random.random() < 0.002:
            payment_amount *= -1

        payment = {
            "payment_id": generate_id(
                "PAY",
                index,
                width=8,
            ),
            "order_id": order["order_id"],
            "payment_date": payment_date.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "payment_method": random.choice(
                PAYMENT_METHODS
            ),
            "payment_amount": round(
                payment_amount,
                2,
            ),
            "currency": "USD",
            "payment_status": payment_status,
            "transaction_reference": (
                f"TXN-{random.randint(100000000, 999999999)}"
            ),
        }

        payments.append(payment)

    dataframe = pd.DataFrame(payments)

    # Add missing transaction references intentionally.
    missing_count = max(
        1,
        int(len(dataframe) * 0.003),
    )

    missing_indices = dataframe.sample(
        n=missing_count,
        random_state=42,
    ).index

    dataframe.loc[
        missing_indices,
        "transaction_reference",
    ] = None

    # Add duplicate payment rows intentionally.
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
        f"Generated payments dataset: "
        f"{len(dataframe):,} rows -> {output_path}"
    )

    return dataframe