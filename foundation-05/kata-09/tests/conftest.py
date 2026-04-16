"""
Shared fixtures for Kata 9 integration tests.

All fixtures that touch the filesystem use pytest's tmp_path, which creates
a unique temporary directory per test and cleans it up automatically after
each test function completes.
"""

import csv
import sqlite3
import sys
from pathlib import Path

import pytest

# Allow `import pipeline` from the kata-09 root
sys.path.insert(0, str(Path(__file__).parent.parent))

# ---------------------------------------------------------------------------
# Path helpers
# ---------------------------------------------------------------------------

KATA_ROOT = Path(__file__).parent.parent
SCHEMA_FILE = KATA_ROOT / "schema.sql"
SAMPLE_CSV = KATA_ROOT / "data" / "raw_gdp.csv"


# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------


@pytest.fixture()
def schema_path() -> Path:
    """Return the canonical schema.sql so tests don't embed raw SQL."""
    assert SCHEMA_FILE.exists(), f"schema.sql not found at {SCHEMA_FILE}"
    return SCHEMA_FILE


@pytest.fixture()
def make_csv(tmp_path: Path):
    """
    Factory fixture: call it with a list of row dicts to write a CSV into
    the test's isolated tmp_path directory.

    Usage::

        def test_foo(make_csv):
            csv_file = make_csv([{"date": "2020-01-01", "value": "1000.0"}])
    """

    def _factory(rows: list[dict], filename: str = "test_gdp.csv") -> Path:
        p = tmp_path / filename
        with p.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["date", "value"])
            writer.writeheader()
            writer.writerows(rows)
        return p

    return _factory


@pytest.fixture()
def pipeline_paths(tmp_path: Path, schema_path: Path):
    """
    Return a dict of all five paths that run_pipeline() needs.
    The db, report, and log paths live inside tmp_path (auto-cleaned).
    """
    return {
        "db_path": tmp_path / "test.db",
        "schema_path": schema_path,
        "report_path": tmp_path / "report.md",
        "log_path": tmp_path / "output" / "validation.log",
    }


@pytest.fixture()
def query_db(pipeline_paths: dict):
    """
    Convenience helper that returns a function to run a SELECT against the
    test database after the pipeline has populated it.
    """

    def _query(sql: str, params: tuple = ()) -> list:
        with sqlite3.connect(pipeline_paths["db_path"]) as conn:
            cur = conn.cursor()
            cur.execute(sql, params)
            return cur.fetchall()

    return _query


# ---------------------------------------------------------------------------
# Data generators
# ---------------------------------------------------------------------------


def make_quarterly_rows(n: int, start_value: float = 15000.0) -> list[dict]:
    """
    Generate *n* quarterly GDP rows with a deterministic 0.5 % quarterly
    growth rate.  Dates begin at 1947-01-01, matching the real FRED series.
    """
    rows = []
    year, month = 1947, 1
    value = start_value
    for _ in range(n):
        rows.append({"date": f"{year:04d}-{month:02d}-01", "value": f"{value:.2f}"})
        value *= 1.005  # 0.5 % growth each quarter
        month += 3
        if month > 12:
            month -= 12
            year += 1
    return rows
