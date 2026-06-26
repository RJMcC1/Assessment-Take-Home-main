"""Shared pytest fixtures for the take-home data pipeline tests."""

from pathlib import Path

import pytest

from process_raw_data import load_author_lookup


@pytest.fixture(scope="session", name="project_root")
def fixture_project_root() -> Path:
    """Return the repository root path for tests."""
    return Path(__file__).resolve().parents[1]


@pytest.fixture(scope="session")
def author_lookup(project_root: Path) -> dict[int, str]:
    """Provide a cached author-id lookup loaded from the test database."""
    return load_author_lookup(project_root / "data" / "authors.db")
