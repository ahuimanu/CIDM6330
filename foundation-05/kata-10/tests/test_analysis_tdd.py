"""
Kata 10 -- TDD test suite for analysis.py

Each function was built via a strict RED -> GREEN -> REFACTOR cycle.
The commit history reflects this: every cycle has three commits labelled
[RED], [GREEN], and [REFACTOR] in that order.
"""

from analysis import detect_contractions  # noqa: E402 (added after RED commit)

# =============================================================================
# TDD CYCLE 1 -- detect_contractions
# =============================================================================


def test_detect_contractions_returns_correct_dates(db_with_known_data):
    """Known dataset has two quarters of negative growth: 2020-07-01 and 2021-01-01."""
    result = detect_contractions(db_with_known_data)
    assert result == ["2020-07-01", "2021-01-01"]


def test_detect_contractions_returns_empty_list_when_none(tmp_path, schema_path):
    """A database with only one row has no growth rates yet -- no contractions."""
    import sqlite3

    db_path = tmp_path / "single.db"
    schema = schema_path.read_text(encoding="utf-8")
    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema)
        conn.execute(
            "INSERT INTO gdp_observations(date, value) VALUES (?, ?)",
            ("2020-01-01", 1000.0),
        )
    result = detect_contractions(db_path)
    assert result == []


def test_detect_contractions_result_is_sorted(db_with_known_data):
    """Contraction dates must be in ascending chronological order."""
    result = detect_contractions(db_with_known_data)
    assert result == sorted(result)
