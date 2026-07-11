from __future__ import annotations

import random
import string
from datetime import datetime, timedelta
from pathlib import Path

import numpy as np

from data_pipeline.data_generator.config import SEED


random.seed(SEED)
np.random.seed(SEED)


def generate_id(prefix: str, number: int, width: int = 6) -> str:
    """
    Create a formatted ID.

    Example:
    generate_id("CUST", 25) -> CUST000025
    """
    return f"{prefix}{number:0{width}d}"


def random_date(
    start_date: datetime,
    end_date: datetime,
) -> datetime:
    """
    Return a random datetime between two dates.
    """
    if start_date > end_date:
        raise ValueError("start_date cannot be later than end_date")

    total_seconds = int((end_date - start_date).total_seconds())
    random_seconds = random.randint(0, total_seconds)

    return start_date + timedelta(seconds=random_seconds)


def random_price(
    minimum: float = 5.0,
    maximum: float = 1000.0,
) -> float:
    """
    Generate a positive price rounded to two decimal places.
    """
    return round(random.uniform(minimum, maximum), 2)


def random_quantity(
    minimum: int = 1,
    maximum: int = 5,
) -> int:
    """
    Generate a random product quantity.
    """
    return random.randint(minimum, maximum)


def random_discount() -> float:
    """
    Generate a realistic discount percentage.
    """
    return random.choice(
        [0.0, 0.0, 0.0, 5.0, 10.0, 15.0, 20.0, 25.0]
    )


def random_boolean(true_probability: float = 0.5) -> bool:
    """
    Return True according to the supplied probability.
    """
    if not 0 <= true_probability <= 1:
        raise ValueError("true_probability must be between 0 and 1")

    return random.random() < true_probability


def generate_invalid_email() -> str:
    """
    Generate intentionally invalid email data for quality testing.
    """
    patterns = [
        "invalid-email",
        "missing-at-symbol.com",
        "@missingusername.com",
        "user@",
        "user name@example.com",
    ]

    return random.choice(patterns)


def add_missing_values(
    values: list,
    probability: float = 0.01,
) -> list:
    """
    Randomly replace a small percentage of values with None.
    """
    if not 0 <= probability <= 1:
        raise ValueError("probability must be between 0 and 1")

    return [
        None if random.random() < probability else value
        for value in values
    ]


def generate_session_id(length: int = 16) -> str:
    """
    Generate a random website session ID.
    """
    characters = string.ascii_uppercase + string.digits

    return "".join(
        random.choices(characters, k=length)
    )


def ensure_output_directory(path: Path) -> None:
    """
    Create the output directory when it does not already exist.
    """
    path.mkdir(parents=True, exist_ok=True)