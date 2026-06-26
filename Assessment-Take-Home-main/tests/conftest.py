from pathlib import Path

import pytest

from process_raw_data import load_author_lookup


@pytest.fixture(scope="session")
def project_root() -> Path:
	return Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def author_lookup(project_root: Path) -> dict[int, str]:
	return load_author_lookup(project_root / "data" / "authors.db")