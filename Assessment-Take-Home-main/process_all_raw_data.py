"""Combine all raw files and write a single PROCESSED_DATA.csv output."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from process_raw_data import load_author_lookup, normalize_dataframe


def get_raw_files(data_dir: Path) -> list[Path]:
    """Return sorted raw CSV files from the data directory."""
    return sorted(data_dir.glob("RAW_DATA_*.csv"))


def process_all_raw_files(project_root: Path) -> pd.DataFrame:
    """Process every data/RAW_DATA_*.csv file into one dataframe."""
    data_dir = project_root / "data"
    raw_files = get_raw_files(data_dir)

    if not raw_files:
        raise FileNotFoundError("No files found matching data/RAW_DATA_*.csv")

    combined_raw = pd.concat((pd.read_csv(path) for path in raw_files), ignore_index=True)
    author_lookup = load_author_lookup(data_dir / "authors.db")
    return normalize_dataframe(combined_raw, author_lookup)


def main() -> None:
    """Process every data/RAW_DATA_*.csv file and write PROCESSED_DATA.csv."""
    project_root = Path(__file__).resolve().parent
    processed = process_all_raw_files(project_root)
    processed.to_csv(project_root / "PROCESSED_DATA.csv", index=False)


if __name__ == "__main__":
    main()
