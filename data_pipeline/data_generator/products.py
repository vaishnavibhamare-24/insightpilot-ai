from __future__ import annotations

import random
from pathlib import Path

import pandas as pd

from data_pipeline.data_generator.config import (
    NUM_PRODUCTS,
    PRODUCT_CATEGORIES,
)
from data_pipeline.data_generator.utils import (
    generate_id,
    random_price,
)


def generate_products(output_path: Path) -> pd.DataFrame:
    """
    Generate a realistic product catalog.
    """
    products: list[dict] = []

    brands = [
        "NovaTech",
        "HomeNest",
        "UrbanPeak",
        "FitCore",
        "PageCraft",
        "GlowWell",
        "FreshMart",
        "DrivePro",
        "PlaySphere",
        "OfficeEdge",
    ]

    for index in range(1, NUM_PRODUCTS + 1):
        category = random.choice(PRODUCT_CATEGORIES)
        unit_price = random_price(5.0, 1500.0)
        unit_cost = round(unit_price * random.uniform(0.35, 0.75), 2)

        product = {
            "product_id": generate_id("PROD", index),
            "product_name": f"{category} Product {index}",
            "category": category,
            "brand": random.choice(brands),
            "unit_price": unit_price,
            "unit_cost": unit_cost,
            "stock_quantity": random.randint(0, 1000),
            "supplier_rating": round(random.uniform(2.5, 5.0), 1),
            "is_active": random.choice([True, True, True, False]),
        }

        products.append(product)

    dataframe = pd.DataFrame(products)

    # Add a few missing values for later quality testing.
    missing_count = max(1, int(NUM_PRODUCTS * 0.01))
    missing_indices = dataframe.sample(
        n=missing_count,
        random_state=42,
    ).index

    dataframe.loc[missing_indices, "brand"] = None

    # Add a few duplicate products intentionally.
    duplicate_count = max(1, int(NUM_PRODUCTS * 0.004))
    duplicate_rows = dataframe.sample(
        n=duplicate_count,
        random_state=7,
    )

    dataframe = pd.concat(
        [dataframe, duplicate_rows],
        ignore_index=True,
    )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    dataframe.to_csv(output_path, index=False)

    print(
        f"Generated products dataset: "
        f"{len(dataframe):,} rows -> {output_path}"
    )

    return dataframe