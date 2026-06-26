"""Process a raw books CSV into PROCESSED_DATA.csv."""

from __future__ import annotations

import argparse
import re
import sqlite3
from pathlib import Path

import pandas as pd

REQUIRED_RAW_COLUMNS = ["book_title", "author_id", "Year released", "Rating", "ratings"]
OUTPUT_COLUMNS = ["title", "author_name", "year", "rating", "ratings"]
CRITICAL_RAW_COLUMNS = ["book_title", "author_id"]


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


def clean_title(title: object | None) -> str:
    """Remove bracketed metadata and normalize title whitespace."""
    if not isinstance(title, str):
        return ""
    cleaned = re.sub(r"\s*[\(\[].*?[\)\]]", "", title)
    return re.sub(r"\s+", " ", cleaned).strip()


def _require_raw_columns(df: pd.DataFrame) -> None:
    """Validate that all required raw input columns are present."""
    missing_columns = [col for col in REQUIRED_RAW_COLUMNS if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Input CSV is missing required columns: {missing_columns}")


def _drop_missing_critical_rows(working: pd.DataFrame) -> pd.DataFrame:
    """Remove rows missing title/author values and normalize string fields."""
    working = working.dropna(subset=CRITICAL_RAW_COLUMNS)
    working["book_title"] = working["book_title"].astype(str).str.strip()
    working["author_id"] = working["author_id"].astype(str).str.strip()
    return working[
        (working["book_title"] != "")
        & (working["book_title"].str.lower() != "nan")
        & (working["author_id"] != "")
        & (working["author_id"].str.lower() != "nan")
    ]


def _normalize_author_names(
    working: pd.DataFrame, author_lookup: dict[int, str]
) -> pd.DataFrame:
    """Coerce author ids, map author names, and drop unknown authors."""
    author_ids = pd.to_numeric(working["author_id"], errors="coerce")
    working["author_id_numeric"] = author_ids.astype("Int64")
    working = working[working["author_id_numeric"].notna()]
    working["author_name"] = working["author_id_numeric"].map(author_lookup)
    return working[working["author_name"].notna()]


def _normalize_numeric_columns(working: pd.DataFrame) -> pd.DataFrame:
    """Normalize and validate year/rating/ratings numeric columns."""
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
    return working


def _finalize_output(working: pd.DataFrame) -> pd.DataFrame:
    """Select output columns, deduplicate rows, and sort by rating."""
    output = working[OUTPUT_COLUMNS].copy()
    output = output.drop_duplicates(subset=OUTPUT_COLUMNS, keep="first")
    return output.sort_values(by="rating", ascending=False, kind="mergesort")


def normalize_dataframe(df: pd.DataFrame, author_lookup: dict[int, str]) -> pd.DataFrame:
    """Apply data cleaning, type conversion, deduplication, and sorting."""
    _require_raw_columns(df)

    working = df[REQUIRED_RAW_COLUMNS].copy()
    working = _drop_missing_critical_rows(working)

    working["title"] = working["book_title"].map(clean_title)
    working = working[working["title"] != ""]

    working = _normalize_author_names(working, author_lookup)
    working = _normalize_numeric_columns(working)
    return _finalize_output(working)


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
