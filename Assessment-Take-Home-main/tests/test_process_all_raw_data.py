from pathlib import Path

import pandas as pd
import pytest

import process_all_raw_data


def test_get_raw_files_returns_sorted_matches(tmp_path: Path) -> None:
	data_dir = tmp_path / "data"
	data_dir.mkdir()
	(data_dir / "RAW_DATA_2.csv").write_text("book_title,author_id,Year released,Rating,ratings\n")
	(data_dir / "RAW_DATA_0.csv").write_text("book_title,author_id,Year released,Rating,ratings\n")
	(data_dir / "not_raw.csv").write_text("ignored\n")

	paths = process_all_raw_data.get_raw_files(data_dir)

	assert [path.name for path in paths] == ["RAW_DATA_0.csv", "RAW_DATA_2.csv"]


def test_process_all_raw_files_raises_when_no_raw_files(tmp_path: Path) -> None:
	project_root = tmp_path
	(project_root / "data").mkdir()

	with pytest.raises(FileNotFoundError, match="No files found matching"):
		process_all_raw_data.process_all_raw_files(project_root)


def test_process_all_raw_files_combines_files_and_calls_normalizer(
	tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
	project_root = tmp_path
	data_dir = project_root / "data"
	data_dir.mkdir()

	pd.DataFrame(
		{
			"book_title": ["A"],
			"author_id": ["1"],
			"Year released": [2001],
			"Rating": [4.5],
			"ratings": [100],
		}
	).to_csv(data_dir / "RAW_DATA_0.csv", index=False)
	pd.DataFrame(
		{
			"book_title": ["B"],
			"author_id": ["2"],
			"Year released": [2002],
			"Rating": [4.0],
			"ratings": [200],
		}
	).to_csv(data_dir / "RAW_DATA_1.csv", index=False)

	captured: dict[str, object] = {}

	def fake_load_author_lookup(db_path: Path) -> dict[int, str]:
		captured["db_path"] = db_path
		return {1: "Author A", 2: "Author B"}

	def fake_normalize_dataframe(
		df: pd.DataFrame, author_lookup: dict[int, str]
	) -> pd.DataFrame:
		captured["rows"] = len(df)
		captured["author_lookup"] = author_lookup
		return pd.DataFrame(
			{
				"title": ["A", "B"],
				"author_name": ["Author A", "Author B"],
				"year": [2001, 2002],
				"rating": [4.5, 4.0],
				"ratings": [100, 200],
			}
		)

	monkeypatch.setattr(process_all_raw_data, "load_author_lookup", fake_load_author_lookup)
	monkeypatch.setattr(process_all_raw_data, "normalize_dataframe", fake_normalize_dataframe)

	result = process_all_raw_data.process_all_raw_files(project_root)

	assert captured["db_path"] == data_dir / "authors.db"
	assert captured["rows"] == 2
	assert captured["author_lookup"] == {1: "Author A", 2: "Author B"}
	assert list(result["title"]) == ["A", "B"]
