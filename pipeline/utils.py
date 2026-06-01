"""Small, pure helpers (easy to unit test) plus logging setup."""
from __future__ import annotations

import logging


def get_logger(name: str) -> logging.Logger:
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
    )
    return logging.getLogger(name)


def clean_gender(value: str | None) -> str | None:
    """Normalize a Synthea gender value to 'M' or 'F', else None."""
    if not value:
        return None
    normalized = value.strip().upper()
    return normalized if normalized in {"M", "F"} else None


def is_active_medication(stop: str | None) -> bool:
    """A medication with no stop date is treated as currently active."""
    return stop is None or str(stop).strip() == ""
