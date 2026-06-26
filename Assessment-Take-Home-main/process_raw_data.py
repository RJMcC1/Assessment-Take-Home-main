"""Process a raw books CSV into PROCESSED_DATA.csv."""

from __future__ import annotations

import argparse
import re
import sqlite3
from pathlib import Path

import pandas as pd

REQUIRED_RAW_COLUMNS = ["book_title", "author_id", "Year released", "Rating", "ratings"]
OUTPUT_COLUMNS = ["title", "author_name", "year", "rating", "ratings"]


def parse_args() -> argparse.Namespace:
	"""Parse command-line arguments."""
	parser = argparse.ArgumentParser(
		description="Clean a raw romance books CSV into PROCESSED_DATA.csv"
	)
	parser.add_argument("input_csv", help="Path to a raw CSV input file")
	return parser.parse_args()


def load_author_lookup(db_path: Path) -> dict[int, str]:
	"""Load author id -> author name mapping from SQLite."""
	if not db_path.exists():
		raise FileNotFoundError(f"Could not find authors DB at {db_path}")

	with sqlite3.connect(db_path) as connection:
		rows = connection.execute("SELECT id, name FROM author").fetchall()
	return {int(author_id): name for author_id, name in rows}


def clean_title(title: str) -> str:
	"""Remove bracketed metadata and normalize title whitespace."""
	if not isinstance(title, str):
		return ""
	cleaned = re.sub(r"\s*[\(\[].*?[\)\]]", "", title)
	return re.sub(r"\s+", " ", cleaned).strip()


def normalize_dataframe(df: pd.DataFrame, author_lookup: dict[int, str]) -> pd.DataFrame:
	"""Apply data cleaning, type conversion, deduplication, and sorting."""
	missing_columns = [col for col in REQUIRED_RAW_COLUMNS if col not in df.columns]
	if missing_columns:
		raise ValueError(f"Input CSV is missing required columns: {missing_columns}")

	working = df[REQUIRED_RAW_COLUMNS].copy()
	working = working.dropna(subset=["book_title", "author_id"])

	# Drop rows with missing/blank critical fields before expensive transforms.
	working["book_title"] = working["book_title"].astype(str).str.strip()
	working["author_id"] = working["author_id"].astype(str).str.strip()
	working = working[
		(working["book_title"] != "")
		& (working["book_title"].str.lower() != "nan")
		& (working["author_id"] != "")
		& (working["author_id"].str.lower() != "nan")
	]

	working["title"] = working["book_title"].map(clean_title)
	working = working[working["title"] != ""]

	author_ids = pd.to_numeric(working["author_id"], errors="coerce")
	working["author_id_numeric"] = author_ids.astype("Int64")
	working = working[working["author_id_numeric"].notna()]
	working["author_name"] = working["author_id_numeric"].map(author_lookup)
	working = working[working["author_name"].notna()]

	working["year"] = pd.to_numeric(working["Year released"], errors="coerce")
	rating_clean = working["Rating"].astype(str).str.replace(",", ".", regex=False).str.strip()
	working["rating"] = pd.to_numeric(rating_clean, errors="coerce")

	ratings_clean = (
		working["ratings"]
		.astype(str)
		.str.replace("`", "", regex=False)
		.str.replace(",", "", regex=False)
		.str.strip()
	)
	working["ratings"] = pd.to_numeric(ratings_clean, errors="coerce")

	working = working.dropna(subset=["year", "rating", "ratings"])
	working["year"] = working["year"].astype(int)
	working["ratings"] = working["ratings"].astype(int)

	output = working[OUTPUT_COLUMNS].copy()
	output = output.drop_duplicates(subset=OUTPUT_COLUMNS, keep="first")
	output = output.sort_values(by="rating", ascending=False, kind="mergesort")
	return output


def main() -> None:
	"""Run processing from CLI and write PROCESSED_DATA.csv."""
	args = parse_args()
	input_path = Path(args.input_csv)
	if not input_path.exists():
		raise FileNotFoundError(f"Input file does not exist: {input_path}")

	project_root = Path(__file__).resolve().parent
	author_lookup = load_author_lookup(project_root / "data" / "authors.db")
	raw_df = pd.read_csv(input_path)
	processed_df = normalize_dataframe(raw_df, author_lookup)

	output_path = project_root / "PROCESSED_DATA.csv"
	processed_df.to_csv(output_path, index=False)


if __name__ == "__main__":
	main()

