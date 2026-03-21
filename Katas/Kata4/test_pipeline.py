import sys
import os
from pathlib import Path
from datetime import datetime

import pytest

# Ensure the kata module directory is importable
sys.path.insert(0, os.path.dirname(__file__))
import pipeline


def make_raw_rows(rows):
    """Helper to create raw CSV-like dict rows (strings)."""
    for r in rows:
        yield {"date": r[0], "value": r[1]}


def test_transform_skips_empty_rows():
    raw = list(make_raw_rows([
        ("2020-01-01", "1.0"),
        ("", "2.0"),
        ("2020-01-02", "")
    ]))

    transformed = list(pipeline.transform(raw))
    assert len(transformed) == 1
    assert transformed[0]["date"] == datetime(2020, 1, 1)
    assert transformed[0]["value"] == 1.0


@pytest.mark.parametrize("bad_date", ["01-01-2020", "20200101", "2020/01/01"])
def test_transform_raises_on_bad_date_format(bad_date):
    raw = list(make_raw_rows([(bad_date, "1.0")]))
    with pytest.raises(ValueError):
        # materialize generator to trigger parsing
        list(pipeline.transform(raw))


def test_load_writes_to_sqlite_and_report(monkeypatch, tmp_path):
    db_file = tmp_path / "test_rates.db"

    transformed = [
        {"date": datetime(2020, 1, 1), "value": 1.5},
        {"date": datetime(2020, 1, 2), "value": 2.5},
    ]

    # Load into DB
    pipeline.load(str(db_file), transformed)

    # Verify DB contents
    import sqlite3

    conn = sqlite3.connect(str(db_file))
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM interest_rates")
    count = cur.fetchone()[0]
    assert count == 2

    cur.execute("SELECT AVG(value) FROM interest_rates")
    avg = cur.fetchone()[0]
    assert abs(avg - 2.0) < 1e-6
    conn.close()

    # Run report in an isolated temp cwd so it writes its report there
    monkeypatch.chdir(tmp_path)
    pipeline.report(str(db_file))

    report_file = tmp_path / "report.md"
    assert report_file.exists()
    text = report_file.read_text()
    assert "Total Records" in text
    assert "Average Rate" in text
