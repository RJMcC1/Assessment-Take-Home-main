from pathlib import Path

import pandas as pd
import pytest

from process_raw_data import OUTPUT_COLUMNS, clean_title, normalize_dataframe


def test_clean_title_removes_bracketed_sections() -> None:
	assert clean_title("Book Title (Series #1)") == "Book Title"
	assert clean_title("Book Title [Paperback]") == "Book Title"
	assert clean_title("Book   Title   (Special)") == "Book Title"


def test_clean_title_handles_non_string_values() -> None:
	assert clean_title(None) == ""
	assert clean_title(42) == ""


def test_normalize_dataframe_requires_expected_columns(author_lookup: dict[int, str]) -> None:
	bad_df = pd.DataFrame({"book_title": ["A"]})

	with pytest.raises(ValueError, match="missing required columns"):
		normalize_dataframe(bad_df, author_lookup)


def test_normalize_dataframe_cleans_and_sorts(author_lookup: dict[int, str]) -> None:
	raw = pd.DataFrame(
		{
			"book_title": [
				"Alpha (Series #1)",
				"",  # should be removed
				"Gamma [Paperback]",
				"Delta",
			],
			"author_id": ["1", "1", "2", "nope"],
			"Year released": ["2001", "2002", "2003", "2004"],
			"Rating": ["4,5", "4.9", "3.2", "5.0"],
			"ratings": ["1,000", "200", "`300`", "500"],
		}
	)

	result = normalize_dataframe(raw, author_lookup)

	assert list(result.columns) == OUTPUT_COLUMNS
	assert result["title"].tolist() == ["Alpha", "Gamma"]
	assert result["rating"].tolist() == [4.5, 3.2]
	assert result["ratings"].tolist() == [1000, 300]
	assert pd.api.types.is_integer_dtype(result["year"])
	assert pd.api.types.is_integer_dtype(result["ratings"])


def test_raw_data_4_matches_expected_records(
	project_root: Path, author_lookup: dict[int, str]
) -> None:
	raw_df = pd.read_csv(project_root / "data" / "RAW_DATA_4.csv")
	expected_df = pd.read_csv(project_root / "data" / "EXAMPLE_DATA_4.csv")
	actual_df = normalize_dataframe(raw_df, author_lookup)

	assert list(actual_df.columns) == OUTPUT_COLUMNS
	assert actual_df["rating"].is_monotonic_decreasing

	# Compare logical content independent of tie-ordering for equal ratings.
	actual_sorted = actual_df.sort_values(
		by=["rating", "title", "author_name", "year", "ratings"],
		ascending=[False, True, True, True, True],
	).reset_index(drop=True)
	expected_sorted = expected_df.sort_values(
		by=["rating", "title", "author_name", "year", "ratings"],
		ascending=[False, True, True, True, True],
	).reset_index(drop=True)

	pd.testing.assert_frame_equal(actual_sorted, expected_sorted, check_dtype=False)