"""Combine all raw files and write a single PROCESSED_DATA.csv output."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from process_raw_data import load_author_lookup, normalize_dataframe


def main() -> None:
	"""Process every data/RAW_DATA_*.csv file into one output dataset."""
	project_root = Path(__file__).resolve().parent
	data_dir = project_root / "data"
	raw_files = sorted(data_dir.glob("RAW_DATA_*.csv"))

	if not raw_files:
		raise FileNotFoundError("No files found matching data/RAW_DATA_*.csv")

	combined_raw = pd.concat((pd.read_csv(path) for path in raw_files), ignore_index=True)
	author_lookup = load_author_lookup(data_dir / "authors.db")
	processed = normalize_dataframe(combined_raw, author_lookup)
	processed.to_csv(project_root / "PROCESSED_DATA.csv", index=False)


if __name__ == "__main__":
	main()
