"""Generate top keyword chart from PROCESSED_DATA.csv."""

from __future__ import annotations

import re
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd

from processed_data_utils import load_processed_data, processed_csv_path, save_current_figure

STOPWORDS = {
    "a",
    "an",
    "and",
    "at",
    "be",
    "but",
    "by",
    "for",
    "from",
    "in",
    "into",
    "is",
    "it",
    "its",
    "of",
    "on",
    "or",
    "s",
    "that",
    "the",
    "their",
    "to",
    "with",
}


def extract_keywords(titles: pd.Series, top_n: int = 20) -> list[tuple[str, int]]:
    """Extract and count normalized keywords from titles."""
    counter: Counter[str] = Counter()

    for title in titles.dropna().astype(str):
        for token in re.findall(r"[A-Za-z]+(?:'[A-Za-z]+)?", title.lower()):
            if len(token) < 3 or token in STOPWORDS:
                continue
            counter[token] += 1

    return counter.most_common(top_n)


def create_top_keywords_chart(df: pd.DataFrame, output_path: Path) -> None:
    """Create sorted bar chart for top title keywords."""
    top_keywords = extract_keywords(df["title"], top_n=20)
    if not top_keywords:
        raise ValueError("No valid title keywords found to build top_keywords.png")

    keywords_df = pd.DataFrame(top_keywords, columns=["keyword", "count"]).sort_values(
        by="count", ascending=True
    )

    plt.figure(figsize=(11, 7))
    plt.barh(keywords_df["keyword"], keywords_df["count"])
    plt.xlabel("Frequency")
    plt.ylabel("Keyword")
    plt.title("Top 20 Keywords in Titles")
    save_current_figure(output_path)


def main() -> None:
    """Generate top_keywords.png from PROCESSED_DATA.csv."""
    processed_csv = processed_csv_path(__file__)
    project_root = processed_csv.parent

    df = load_processed_data(processed_csv, required_columns={"title"})
    create_top_keywords_chart(df, project_root / "top_keywords.png")


if __name__ == "__main__":
    main()
