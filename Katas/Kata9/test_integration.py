"""
Integration tests for the Kata4 pipeline (pipeline.py copied here from Kata4).

WHY SYNTHETIC DATA instead of the real FEDFUNDS.csv:
  - The real file lives at an absolute path on one machine; tests would break on
    any other machine or in CI without that exact file present.
  - Synthetic data lets us control *exactly* what goes in so we can assert
    *exactly* what should come out — no ambiguity about expected averages, counts,
    or date ranges.
  - For volume testing we generate 1 000 rows programmatically, which satisfies
    the "real-ish data volume" requirement without a file dependency.
"""

import csv
import sqlite3
import sys
import os
from datetime import datetime, timedelta
from pathlib import Path

import pytest

sys.path.insert(0, os.path.dirname(__file__))
import pipeline


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def write_csv(path: Path, rows: list[dict]) -> None:
    """Write a list of dicts as a CSV file with FRED-style columns."""
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["date", "realtime_start", "realtime_end", "value"])
        writer.writeheader()
        writer.writerows(rows)


def make_fred_rows(n: int, start_date: str = "1990-01-01", base_value: float = 5.0) -> list[dict]:
    """
    Generate *n* synthetic FRED-style rows starting from start_date.
    Values cycle gently around base_value so statistics are predictable.
    """
    rows = []
    current = datetime.strptime(start_date, "%Y-%m-%d")
    for i in range(n):
        rows.append({
            "date": current.strftime("%Y-%m-%d"),
            "realtime_start": "2026-01-01",
            "realtime_end": "2026-01-01",
            "value": round(base_value + (i % 10) * 0.1, 2),
        })
        current += timedelta(days=30)
    return rows


# ---------------------------------------------------------------------------
# Test 1 — Full pipeline: CSV → DB → report (small, known data)
# ---------------------------------------------------------------------------

def test_full_pipeline_end_to_end(tmp_path, monkeypatch):
    """
    Happy-path integration test.
    Feed known rows through the entire pipeline and verify every output.
    """
    rows = [
        {"date": "2000-01-01", "realtime_start": "2026-01-01", "realtime_end": "2026-01-01", "value": "2.0"},
        {"date": "2000-02-01", "realtime_start": "2026-01-01", "realtime_end": "2026-01-01", "value": "4.0"},
        {"date": "2000-03-01", "realtime_start": "2026-01-01", "realtime_end": "2026-01-01", "value": "6.0"},
    ]

    csv_path = tmp_path / "input.csv"
    db_path = tmp_path / "rates.db"
    write_csv(csv_path, rows)

    # Run pipeline (report writes report.md relative to cwd)
    monkeypatch.chdir(tmp_path)
    pipeline.main(str(csv_path), str(db_path))

    # --- Verify DB ---
    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM interest_rates")
    assert cur.fetchone()[0] == 3, "All 3 rows should be loaded"

    cur.execute("SELECT AVG(value) FROM interest_rates")
    assert abs(cur.fetchone()[0] - 4.0) < 1e-9, "Average of [2, 4, 6] should be 4.0"

    cur.execute("SELECT MIN(date), MAX(date) FROM interest_rates")
    min_d, max_d = cur.fetchone()
    assert min_d == "2000-01-01"
    assert max_d == "2000-03-01"
    conn.close()

    # --- Verify report.md ---
    report_path = tmp_path / "report.md"
    assert report_path.exists(), "report.md must be created"
    text = report_path.read_text()
    assert "Total Records**: 3" in text
    assert "Average Rate**: 4.00%" in text
    assert "Maximum Rate**: 6.00%" in text
    assert "2000-01-01" in text
    assert "2000-03-01" in text


# ---------------------------------------------------------------------------
# Test 2 — Dirty input: bad rows are filtered, clean rows survive
# ---------------------------------------------------------------------------

def test_pipeline_skips_malformed_rows(tmp_path, monkeypatch):
    """
    Rows with missing date or value must be silently dropped.
    Only well-formed rows should reach the database.
    """
    rows = [
        {"date": "2010-01-01", "realtime_start": "", "realtime_end": "", "value": "3.5"},
        {"date": "",           "realtime_start": "", "realtime_end": "", "value": "1.0"},  # bad date
        {"date": "2010-03-01", "realtime_start": "", "realtime_end": "", "value": ""},    # bad value
        {"date": "2010-04-01", "realtime_start": "", "realtime_end": "", "value": "7.0"},
    ]
    csv_path = tmp_path / "dirty.csv"
    db_path  = tmp_path / "dirty.db"
    write_csv(csv_path, rows)

    monkeypatch.chdir(tmp_path)
    pipeline.main(str(csv_path), str(db_path))

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM interest_rates")
    assert cur.fetchone()[0] == 2, "Only the 2 clean rows should be in the DB"
    conn.close()


# ---------------------------------------------------------------------------
# Test 3 — Idempotency: running the pipeline twice must not duplicate rows
# ---------------------------------------------------------------------------

def test_pipeline_is_idempotent(tmp_path, monkeypatch):
    """
    INSERT OR REPLACE ensures re-running with the same CSV does not
    create duplicate records.
    """
    rows = [
        {"date": "2005-06-01", "realtime_start": "", "realtime_end": "", "value": "5.25"},
    ]
    csv_path = tmp_path / "input.csv"
    db_path  = tmp_path / "rates.db"
    write_csv(csv_path, rows)

    monkeypatch.chdir(tmp_path)
    pipeline.main(str(csv_path), str(db_path))
    pipeline.main(str(csv_path), str(db_path))  # run again

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM interest_rates")
    assert cur.fetchone()[0] == 1, "Duplicate run must not insert extra rows"
    conn.close()


# ---------------------------------------------------------------------------
# Test 4 — Volume: 1 000 synthetic rows (real-ish data scale)
#
# WHY 1 000 rows and not the actual FEDFUNDS.csv?
#   The real file (~860 rows) lives at a machine-specific absolute path.
#   Synthetic generation keeps tests portable, hermetic, and runnable in CI
#   without any external file dependency, while still exercising the pipeline
#   at a realistic data scale.
# ---------------------------------------------------------------------------

def test_pipeline_volume_1000_rows(tmp_path, monkeypatch):
    """
    Pipeline must handle 1 000 rows correctly end-to-end.
    Verifies count, date range, and a mathematically known average.
    """
    n = 1000
    base = 5.0
    synthetic_rows = make_fred_rows(n, start_date="1940-01-01", base_value=base)

    csv_path = tmp_path / "volume.csv"
    db_path  = tmp_path / "volume.db"
    write_csv(csv_path, synthetic_rows)

    monkeypatch.chdir(tmp_path)
    pipeline.main(str(csv_path), str(db_path))

    conn = sqlite3.connect(str(db_path))
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM interest_rates")
    assert cur.fetchone()[0] == n, f"All {n} rows must be loaded"

    # Values cycle through base + 0.0, 0.1, ..., 0.9 repeatedly.
    # Mean of one full cycle = base + (0+1+…+9)*0.1/10 = base + 0.45
    cur.execute("SELECT AVG(value) FROM interest_rates")
    avg = cur.fetchone()[0]
    assert abs(avg - (base + 0.45)) < 1e-6, f"Expected avg {base + 0.45}, got {avg}"

    cur.execute("SELECT MIN(date), MAX(date) FROM interest_rates")
    min_d, max_d = cur.fetchone()
    assert min_d == "1940-01-01"
    conn.close()

    # Report must also exist and mention all 1 000 records
    report_path = tmp_path / "report.md"
    assert report_path.exists()
    assert "1000" in report_path.read_text()


# ---------------------------------------------------------------------------
# Test 5 — Empty input: pipeline must not crash on an empty CSV
# ---------------------------------------------------------------------------

def test_pipeline_empty_csv(tmp_path, monkeypatch):
    """
    An empty CSV (header only) should produce an empty DB table and a
    report that reflects zero records (AVG will be None — pipeline must
    not crash).
    """
    csv_path = tmp_path / "empty.csv"
    db_path  = tmp_path / "empty.db"

    # Write header-only CSV
    with open(csv_path, "w", newline="") as f:
        csv.DictWriter(f, fieldnames=["date", "realtime_start", "realtime_end", "value"]).writeheader()

    monkeypatch.chdir(tmp_path)

    # The report function calls f.write(f"- **Average Rate**: {average_rate:.2f}%\n")
    # which will crash if average_rate is None.  This test documents that
    # behaviour — update the assertion if/when the pipeline is hardened.
    with pytest.raises((TypeError, AttributeError)):
        pipeline.main(str(csv_path), str(db_path))
