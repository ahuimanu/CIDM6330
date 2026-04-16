"""
Kata 10 -- TDD test suite for analysis.py

Each function was built via a strict RED -> GREEN -> REFACTOR cycle.
The commit history reflects this: every cycle has three commits labelled
[RED], [GREEN], and [REFACTOR] in that order.
"""

import sqlite3

import pytest

from analysis import compute_peak_trough, detect_contractions, generate_summary_report
from pipeline import generate_report, init_db

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


# =============================================================================
# TDD CYCLE 2 -- compute_peak_trough
# =============================================================================


def test_compute_peak_trough_peak_values(db_with_known_data):
    """Peak must be the date + value of the highest GDP observation."""
    result = compute_peak_trough(db_with_known_data)
    assert result.peak_date == "2020-10-01"
    assert result.peak_value == pytest.approx(1188.0)


def test_compute_peak_trough_trough_values(db_with_known_data):
    """Trough must be the date + value of the lowest GDP observation."""
    result = compute_peak_trough(db_with_known_data)
    assert result.trough_date == "2020-07-01"
    assert result.trough_value == pytest.approx(990.0)


def test_compute_peak_trough_peak_above_trough(db_with_known_data):
    """Sanity check: peak value must always exceed trough value."""
    result = compute_peak_trough(db_with_known_data)
    assert result.peak_value > result.trough_value


# =============================================================================
# TDD CYCLE 3 -- generate_summary_report
# =============================================================================


def test_generate_summary_report_creates_file(db_with_known_data, tmp_path):
    """Report file must be written to the given path."""
    report_path = tmp_path / "summary.md"
    generate_summary_report(db_with_known_data, report_path)
    assert report_path.exists()


def test_generate_summary_report_contains_required_sections(db_with_known_data, tmp_path):
    """Report must include a title, Contractions section, Peak, and Trough."""
    report_path = tmp_path / "summary.md"
    generate_summary_report(db_with_known_data, report_path)
    text = report_path.read_text(encoding="utf-8")
    assert "# GDP Analysis Summary" in text
    assert "## Contractions" in text
    assert "## Peak" in text
    assert "## Trough" in text


def test_generate_summary_report_contraction_dates_in_report(db_with_known_data, tmp_path):
    """Both known contraction dates must appear in the report body."""
    report_path = tmp_path / "summary.md"
    generate_summary_report(db_with_known_data, report_path)
    text = report_path.read_text(encoding="utf-8")
    assert "2020-07-01" in text
    assert "2021-01-01" in text


def test_generate_summary_report_peak_trough_values_in_report(db_with_known_data, tmp_path):
    """Peak (1188.00) and trough (990.00) values must appear formatted in the report."""
    report_path = tmp_path / "summary.md"
    generate_summary_report(db_with_known_data, report_path)
    text = report_path.read_text(encoding="utf-8")
    assert "1188.00" in text
    assert "990.00" in text


# =============================================================================
# STRETCH -- Bug-fix TDD: pipeline.generate_report crashes on empty database
#
# Bug: when the gdp_observations table has zero rows, SQLite's aggregate
# functions (MIN/MAX/AVG) return NULL.  Python receives None for each, and
# the f-string formatter `:.2f` raises TypeError on None.
# =============================================================================


def test_generate_report_does_not_crash_on_empty_database(tmp_path, schema_path):
    """[RED] generate_report must not raise TypeError when the DB is empty."""
    db_path = tmp_path / "empty.db"
    init_db(db_path, schema_path)  # creates table, inserts nothing
    report_path = tmp_path / "report.md"
    generate_report(db_path, report_path)  # must not raise
    text = report_path.read_text(encoding="utf-8")
    assert "**0**" in text  # zero rows reported
