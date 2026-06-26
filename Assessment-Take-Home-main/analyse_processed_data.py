"""Analyse PROCESSED_DATA.csv and produce required visualizations."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from processed_data_utils import (
    PROCESSED_REQUIRED_COLUMNS,
    load_processed_data,
    processed_csv_path,
    save_current_figure,
)


def create_decade_releases_chart(df: pd.DataFrame, output_path: Path) -> None:
    """Create pie chart of release proportions by decade."""
    years = pd.to_numeric(df["year"], errors="coerce").dropna().astype(int)
    decades = (years // 10) * 10
    counts = decades.value_counts().sort_index()

    if counts.empty:
        raise ValueError("No valid year values found to build decade_releases.png")

    labels = [f"{decade}s" for decade in counts.index]
    plt.figure(figsize=(8, 8))
    plt.pie(counts.values, labels=labels, autopct="%1.1f%%", startangle=140)
    plt.title("Release Proportion by Decade")
    save_current_figure(output_path)


def get_top_authors_by_ratings(df: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    """Return a deterministically ordered top-authors aggregate dataframe."""
    working = df.copy()
    working["ratings"] = pd.to_numeric(working["ratings"], errors="coerce")
    working = working.dropna(subset=["author_name", "ratings"])

    return (
        working.groupby("author_name", as_index=False)["ratings"]
        .sum()
        .sort_values(by=["ratings", "author_name"], ascending=[False, True])
        .head(limit)
        .sort_values(by=["ratings", "author_name"], ascending=[True, True])
    )


def create_top_authors_chart(df: pd.DataFrame, output_path: Path) -> None:
    """Create sorted bar chart of total ratings for top 10 authors."""
    top_authors = get_top_authors_by_ratings(df, limit=10)

    if top_authors.empty:
        raise ValueError("No valid author/ratings data found to build top_authors.png")

    plt.figure(figsize=(10, 6))
    plt.barh(top_authors["author_name"], top_authors["ratings"])
    plt.xlabel("Total Ratings")
    plt.ylabel("Author")
    plt.title("Top 10 Authors by Total Ratings")
    save_current_figure(output_path)


def main() -> None:
    """Generate required analysis chart outputs."""
    processed_csv = processed_csv_path(__file__)
    project_root = processed_csv.parent

    df = load_processed_data(processed_csv, required_columns=PROCESSED_REQUIRED_COLUMNS)
    create_decade_releases_chart(df, project_root / "decade_releases.png")
    create_top_authors_chart(df, project_root / "top_authors.png")


if __name__ == "__main__":
    main()
