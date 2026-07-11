from __future__ import annotations

import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from data_pipeline.data_generator.config import (
    NUM_ORDERS,
    ORDER_STATUS,
)
from data_pipeline.data_generator.utils import (
    generate_id,
    random_date,
    random_discount,
    random_quantity,
)


def generate_orders(
    customers_df: pd.DataFrame,
    products_df: pd.DataFrame,
    output_path: Path,
) -> pd.DataFrame:
    """
    Generate orders linked to valid customers and products.
    A small amount of intentionally bad data is included for
    later data-quality testing.
    """
    orders: list[dict] = []

    customer_ids = (
        customers_df["customer_id"]
        .dropna()
        .drop_duplicates()
        .tolist()
    )

    product_records = (
        products_df[
            ["product_id", "unit_price"]
        ]
        .drop_duplicates(subset=["product_id"])
        .to_dict("records")
    )

    order_start = datetime(2023, 1, 1)
    order_end = datetime(2026, 6, 30)

    for index in range(1, NUM_ORDERS + 1):
        product = random.choice(product_records)
        quantity = random_quantity(1, 5)
        unit_price = float(product["unit_price"])
        discount_percent = random_discount()

        gross_amount = quantity * unit_price
        discount_amount = gross_amount * (
            discount_percent / 100
        )
        order_amount = round(
            gross_amount - discount_amount,
            2,
        )

        order_date = random_date(
            order_start,
            order_end,
        )

        # Add a small number of future dates intentionally.
        if random.random() < 0.005:
            order_date = datetime.now() + timedelta(
                days=random.randint(1, 60)
            )

        order = {
            "order_id": generate_id("ORD", index, width=8),
            "customer_id": random.choice(customer_ids),
            "product_id": product["product_id"],
            "order_date": order_date.strftime(
                "%Y-%m-%d"
            ),
            "quantity": quantity,
            "unit_price": unit_price,
            "discount_percent": discount_percent,
            "order_amount": order_amount,
            "currency": "USD",
            "order_status": random.choice(
                ORDER_STATUS
            ),
            "sales_channel": random.choice(
                [
                    "Website",
                    "Mobile App",
                    "Marketplace",
                    "Retail Store",
                ]
            ),
            "shipping_method": random.choice(
                [
                    "Standard",
                    "Express",
                    "Same Day",
                    "Store Pickup",
                ]
            ),
        }

        orders.append(order)

    dataframe = pd.DataFrame(orders)

    # Add missing customer IDs intentionally.
    missing_customer_count = max(
        1,
        int(NUM_ORDERS * 0.002),
    )

    missing_indices = dataframe.sample(
        n=missing_customer_count,
        random_state=42,
    ).index

    dataframe.loc[
        missing_indices,
        "customer_id",
    ] = None

    # Add a few negative order amounts intentionally.
    negative_count = max(
        1,
        int(NUM_ORDERS * 0.001),
    )

    negative_indices = dataframe.sample(
        n=negative_count,
        random_state=11,
    ).index

    dataframe.loc[
        negative_indices,
        "order_amount",
    ] *= -1

    # Add duplicate rows intentionally.
    duplicate_count = max(
        1,
        int(NUM_ORDERS * 0.003),
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
        f"Generated orders dataset: "
        f"{len(dataframe):,} rows -> {output_path}"
    )

    return dataframe