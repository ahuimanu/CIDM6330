"""
Shared fixtures for Kata 10 TDD tests.

The `db_with_known_data` fixture builds a populated gdp_observations table
with predictable values so every assertion in the test suite can be verified
by hand without running the pipeline.

Known dataset
-------------
date         value     growth_rate
2020-01-01   1000.0    NULL
2020-04-01   1100.0    +10.0 %
2020-07-01    990.0    -10.0 %   <- contraction
2020-10-01   1188.0    +20.0 %
2021-01-01   1069.2    -10.0 %   <- contraction
2021-04-01   1176.12   +10.0 %

Peak:   2020-10-01, 1188.0
Trough: 2020-07-01,  990.0
Contractions: ["2020-07-01", "2021-01-01"]
"""

import sqlite3
import sys
from pathlib import Path

import pytest

KATA_09 = Path(__file__).parent.parent.parent / "kata-09"
KATA_10 = Path(__file__).parent.parent

sys.path.insert(0, str(KATA_09))
sys.path.insert(0, str(KATA_10))

SCHEMA_PATH = KATA_09 / "schema.sql"

KNOWN_ROWS: list[tuple[str, float]] = [
    ("2020-01-01", 1000.00),
    ("2020-04-01", 1100.00),
    ("2020-07-01",  990.00),
    ("2020-10-01", 1188.00),
    ("2021-01-01", 1069.20),
    ("2021-04-01", 1176.12),
]


@pytest.fixture()
def schema_path() -> Path:
    assert SCHEMA_PATH.exists(), f"schema.sql missing at {SCHEMA_PATH}"
    return SCHEMA_PATH


@pytest.fixture()
def db_with_known_data(tmp_path: Path) -> Path:
    """Populate a temp SQLite database with the known dataset above."""
    db_path = tmp_path / "analysis_test.db"
    schema_sql = SCHEMA_PATH.read_text(encoding="utf-8")

    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema_sql)
        conn.executemany(
            "INSERT INTO gdp_observations(date, value) VALUES (?, ?)", KNOWN_ROWS
        )

    from pipeline import compute_growth_rates  # reuse kata-09 logic

    compute_growth_rates(db_path)
    return db_path
