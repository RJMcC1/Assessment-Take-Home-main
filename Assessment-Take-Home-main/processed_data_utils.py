"""Shared utilities for reading and validating PROCESSED_DATA.csv."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

PROCESSED_REQUIRED_COLUMNS = {"title", "author_name", "year", "rating", "ratings"}


def load_processed_data(
    csv_path: Path, required_columns: set[str] | None = None
) -> pd.DataFrame:
    """Load a processed CSV file and validate required columns."""
    if not csv_path.exists():
        raise FileNotFoundError(f"Could not find processed data file: {csv_path}")

    df = pd.read_csv(csv_path)
    expected_columns = required_columns or PROCESSED_REQUIRED_COLUMNS
    missing_columns = expected_columns.difference(df.columns)
    if missing_columns:
        raise ValueError(f"PROCESSED_DATA.csv missing required columns: {sorted(missing_columns)}")

    return df
