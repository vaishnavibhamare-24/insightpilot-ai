from __future__ import annotations

import random
from datetime import datetime
from pathlib import Path

import pandas as pd

from data_pipeline.data_generator.config import (
    NUM_CUSTOMERS,
    fake,
)
from data_pipeline.data_generator.utils import (
    add_missing_values,
    generate_id,
    generate_invalid_email,
    random_date,
)


def generate_customers(output_path: Path) -> pd.DataFrame:
    """
    Generate a realistic customer dataset with a small amount of
    intentionally bad data for later data-quality testing.
    """
    customers: list[dict] = []

    signup_start = datetime(2021, 1, 1)
    signup_end = datetime(2026, 6, 30)

    for index in range(1, NUM_CUSTOMERS + 1):
        first_name = fake.first_name()
        last_name = fake.last_name()

        email = (
            generate_invalid_email()
            if random.random() < 0.01
            else fake.unique.email()
        )

        customer = {
            "customer_id": generate_id("CUST", index),
            "first_name": first_name,
            "last_name": last_name,
            "email": email,
            "phone": fake.phone_number(),
            "address": fake.street_address(),
            "city": fake.city(),
            "state": fake.state_abbr(),
            "postal_code": fake.postcode(),
            "country": "United States",
            "region": random.choice(
                ["Northeast", "Midwest", "South", "West"]
            ),
            "signup_date": random_date(
                signup_start,
                signup_end,
            ).strftime("%Y-%m-%d"),
            "customer_segment": random.choice(
                ["Standard", "Premium", "Enterprise"]
            ),
            "marketing_opt_in": random.choice([True, False]),
        }

        customers.append(customer)

    dataframe = pd.DataFrame(customers)

    # Intentionally introduce a small number of missing values.
    dataframe["phone"] = add_missing_values(
        dataframe["phone"].tolist(),
        probability=0.02,
    )

    dataframe["state"] = add_missing_values(
        dataframe["state"].tolist(),
        probability=0.01,
    )

    # Add a few duplicate records for later quality testing.
    duplicate_count = max(1, int(NUM_CUSTOMERS * 0.005))
    duplicate_rows = dataframe.sample(
        n=duplicate_count,
        random_state=42,
    )

    dataframe = pd.concat(
        [dataframe, duplicate_rows],
        ignore_index=True,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_path, index=False)

    print(
        f"Generated customers dataset: "
        f"{len(dataframe):,} rows -> {output_path}"
    )

    return dataframe