from __future__ import annotations

import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from data_pipeline.data_generator.config import (
    NUM_WEBSITE_EVENTS,
    WEBSITE_EVENTS,
)
from data_pipeline.data_generator.utils import (
    generate_id,
    generate_session_id,
)


def generate_website_events(
    customers_df: pd.DataFrame,
    products_df: pd.DataFrame,
    output_path: Path,
) -> pd.DataFrame:
    """
    Generate website events linked to customers and products.
    """
    events: list[dict] = []

    customer_ids = (
        customers_df["customer_id"]
        .dropna()
        .drop_duplicates()
        .tolist()
    )

    product_ids = (
        products_df["product_id"]
        .dropna()
        .drop_duplicates()
        .tolist()
    )

    devices = [
        "Desktop",
        "Mobile",
        "Tablet",
    ]

    browsers = [
        "Chrome",
        "Safari",
        "Edge",
        "Firefox",
    ]

    traffic_sources = [
        "Organic Search",
        "Paid Search",
        "Email",
        "Social Media",
        "Direct",
        "Referral",
    ]

    event_start = datetime(2023, 1, 1)
    event_end = datetime(2026, 6, 30)

    total_seconds = int(
        (event_end - event_start).total_seconds()
    )

    for index in range(1, NUM_WEBSITE_EVENTS + 1):
        event_type = random.choice(WEBSITE_EVENTS)

        event_timestamp = event_start + timedelta(
            seconds=random.randint(0, total_seconds)
        )

        product_id = (
            random.choice(product_ids)
            if event_type
            in [
                "Product View",
                "Add To Cart",
                "Checkout",
                "Purchase",
            ]
            else None
        )

        event = {
            "event_id": generate_id(
                "EVT",
                index,
                width=9,
            ),
            "session_id": generate_session_id(),
            "customer_id": (
                random.choice(customer_ids)
                if random.random() < 0.85
                else None
            ),
            "product_id": product_id,
            "event_type": event_type,
            "event_timestamp": event_timestamp.strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "device_type": random.choice(devices),
            "browser": random.choice(browsers),
            "traffic_source": random.choice(
                traffic_sources
            ),
            "page_url": random.choice(
                [
                    "/",
                    "/products",
                    "/cart",
                    "/checkout",
                    "/account",
                    "/support",
                ]
            ),
            "time_on_page_seconds": random.randint(
                1,
                900,
            ),
            "converted": (
                True
                if event_type == "Purchase"
                else False
            ),
        }

        events.append(event)

    dataframe = pd.DataFrame(events)

    # Add missing traffic sources intentionally.
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
        "traffic_source",
    ] = None

    # Add a few future timestamps intentionally.
    future_count = max(
        1,
        int(len(dataframe) * 0.002),
    )

    future_indices = dataframe.sample(
        n=future_count,
        random_state=11,
    ).index

    future_timestamps = [
        (
            datetime.now()
            + timedelta(days=random.randint(1, 30))
        ).strftime("%Y-%m-%d %H:%M:%S")
        for _ in range(future_count)
    ]

    dataframe.loc[
        future_indices,
        "event_timestamp",
    ] = future_timestamps

    # Add duplicate events intentionally.
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
        f"Generated website events dataset: "
        f"{len(dataframe):,} rows -> {output_path}"
    )

    return dataframe