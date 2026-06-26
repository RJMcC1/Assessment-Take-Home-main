"""Tests for title keyword extraction and keyword chart generation."""

from pathlib import Path

import pandas as pd
import pytest

from get_keywords import create_top_keywords_chart, extract_keywords
from processed_data_utils import load_processed_data


def test_extract_keywords_filters_stopwords_and_short_tokens() -> None:
    """Keyword extraction should remove stopwords and short tokens."""
    titles = pd.Series(["The Love in Paris", "Love and Love", "An Us by Sea"])
    result = extract_keywords(titles, top_n=3)

    assert result[0] == ("love", 3)
    keywords = [keyword for keyword, _ in result]
    assert "the" not in keywords
    assert "an" not in keywords
    assert "us" not in keywords


def test_create_top_keywords_chart_writes_png(tmp_path: Path) -> None:
    """Keyword chart generation should write a non-empty PNG file."""
    df = pd.DataFrame({"title": ["Summer Love", "Winter Love", "Autumn Hearts"]})
    output_path = tmp_path / "top_keywords.png"

    create_top_keywords_chart(df, output_path)

    assert output_path.exists()
    assert output_path.stat().st_size > 0


def test_create_top_keywords_chart_raises_when_no_keywords(tmp_path: Path) -> None:
    """Keyword chart generation should fail when no valid keywords are found."""
    df = pd.DataFrame({"title": ["an and the", "of in to", "by or at"]})

    with pytest.raises(ValueError, match="No valid title keywords"):
        create_top_keywords_chart(df, tmp_path / "top_keywords.png")


def test_load_processed_data_can_validate_single_required_column(tmp_path: Path) -> None:
    """Shared loader should enforce custom required columns when provided."""
    csv_path = tmp_path / "PROCESSED_DATA.csv"
    pd.DataFrame({"author_name": ["A"]}).to_csv(csv_path, index=False)

    with pytest.raises(ValueError, match="missing required columns"):
        load_processed_data(csv_path, required_columns={"title"})
