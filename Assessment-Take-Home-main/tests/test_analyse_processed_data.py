"""Tests for processed-data analysis and chart generation."""

from pathlib import Path

import pandas as pd
import pytest

from analyse_processed_data import (
    create_decade_releases_chart,
    create_top_authors_chart,
    get_top_authors_by_ratings,
    load_processed_data,
)


def test_load_processed_data_raises_for_missing_file(tmp_path: Path) -> None:
    """Loading should raise when the processed CSV does not exist."""
    with pytest.raises(FileNotFoundError):
        load_processed_data(tmp_path / "missing.csv")


def test_load_processed_data_raises_for_missing_columns(tmp_path: Path) -> None:
    """Loading should raise when required columns are absent."""
    bad_csv = tmp_path / "PROCESSED_DATA.csv"
    pd.DataFrame({"title": ["A"]}).to_csv(bad_csv, index=False)

    with pytest.raises(ValueError, match="missing required columns"):
        load_processed_data(bad_csv)


def test_create_decade_releases_chart_writes_png(tmp_path: Path) -> None:
    """Decade chart generation should write a non-empty PNG file."""
    df = pd.DataFrame(
        {
            "title": ["A", "B", "C", "D"],
            "author_name": ["Author 1", "Author 2", "Author 1", "Author 3"],
            "year": [1992, 1998, 2004, 2011],
            "rating": [4.1, 3.9, 4.4, 4.0],
            "ratings": [100, 200, 300, 400],
        }
    )

    output_path = tmp_path / "decade_releases.png"
    create_decade_releases_chart(df, output_path)

    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_create_decade_releases_chart_raises_for_invalid_years(tmp_path: Path) -> None:
    """Decade chart should fail when no valid year values exist."""
    df = pd.DataFrame(
        {
            "title": ["A"],
            "author_name": ["Author"],
            "year": ["unknown"],
            "rating": [4.1],
            "ratings": [100],
        }
    )

    with pytest.raises(ValueError, match="No valid year values"):
        create_decade_releases_chart(df, tmp_path / "decade_releases.png")


def test_create_top_authors_chart_writes_png(tmp_path: Path) -> None:
    """Top-authors chart generation should write a non-empty PNG file."""
    df = pd.DataFrame(
        {
            "title": [f"Book {index}" for index in range(12)],
            "author_name": [f"Author {index}" for index in range(12)],
            "year": [2000 + index for index in range(12)],
            "rating": [4.0 for _ in range(12)],
            "ratings": [100 + index for index in range(12)],
        }
    )

    output_path = tmp_path / "top_authors.png"
    create_top_authors_chart(df, output_path)

    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_create_top_authors_chart_raises_for_invalid_rows(tmp_path: Path) -> None:
    """Top-authors chart should fail when no valid author/ratings rows exist."""
    df = pd.DataFrame(
        {
            "title": ["A"],
            "author_name": [None],
            "year": [2001],
            "rating": [4.0],
            "ratings": ["not_a_number"],
        }
    )

    with pytest.raises(ValueError, match="No valid author/ratings data"):
        create_top_authors_chart(df, tmp_path / "top_authors.png")


def test_get_top_authors_by_ratings_has_deterministic_tie_order() -> None:
    """Tie totals should be ordered deterministically by author name."""
    df = pd.DataFrame(
        {
            "title": ["A", "B", "C", "D"],
            "author_name": ["Zoe", "Amy", "Zoe", "Amy"],
            "year": [2001, 2002, 2003, 2004],
            "rating": [4.0, 4.0, 4.1, 4.2],
            "ratings": [100, 100, 50, 50],
        }
    )

    result = get_top_authors_by_ratings(df, limit=10)

    # Both authors total 150 ratings; alphabetical tie-breaker keeps deterministic order.
    assert result["author_name"].tolist() == ["Amy", "Zoe"]
    assert result["ratings"].tolist() == [150, 150]
