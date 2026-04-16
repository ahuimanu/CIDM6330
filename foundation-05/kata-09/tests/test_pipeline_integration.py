"""
Kata 9 -- Integration Tests for the GDP Data Pipeline (Kata 4)
==============================================================

These tests exercise the *full pipeline* end-to-end:
  input CSV  ->  SQLite database  ->  Markdown report

Each test runs in its own isolated tmp_path directory (auto-cleaned by
pytest), so no test can contaminate another and no manual teardown is needed.

Test inventory
--------------
1.  test_full_pipeline_smoke              -- happy path, minimal data
2.  test_exact_row_count_loaded           -- CSV row count == DB row count
3.  test_db_values_match_input            -- DB values == CSV values (exact)
4.  test_first_row_growth_rate_is_null    -- no previous value -> NULL
5.  test_growth_rate_computation          -- known inputs -> known growth %
6.  test_report_exists_and_has_sections  -- report file written with correct structure
7.  test_report_statistics_accuracy      -- report stats match DB aggregates
8.  test_invalid_rows_skipped_and_logged  -- bad rows excluded + logged
9.  test_missing_date_rows_logged         -- empty-date rows excluded + logged
10. test_idempotent_pipeline              -- running twice yields no duplicates
11. test_dry_run_writes_nothing           -- dry_run=True -> no files created
12. test_large_volume_1000_rows           -- 1 000-row load, all growth rates set
"""

import sqlite3

import pytest
from pipeline import run_pipeline

from tests.conftest import make_quarterly_rows

# ---------------------------------------------------------------------------
# 1. Smoke test -- minimal valid data, pipeline returns exit code 0
# ---------------------------------------------------------------------------


def test_full_pipeline_smoke(make_csv, pipeline_paths):
    rows = [
        {"date": "2020-01-01", "value": "1000.00"},
        {"date": "2020-04-01", "value": "1010.00"},
        {"date": "2020-07-01", "value": "1020.10"},
    ]
    csv_file = make_csv(rows)

    exit_code = run_pipeline(
        raw_csv=csv_file,
        db_path=pipeline_paths["db_path"],
        schema_path=pipeline_paths["schema_path"],
        report_path=pipeline_paths["report_path"],
        log_path=pipeline_paths["log_path"],
    )

    assert exit_code == 0
    assert pipeline_paths["db_path"].exists()
    assert pipeline_paths["report_path"].exists()


# ---------------------------------------------------------------------------
# 2. Row count in DB exactly matches number of valid CSV rows
# ---------------------------------------------------------------------------


def test_exact_row_count_loaded(make_csv, pipeline_paths):
    rows = [{"date": f"2021-{m:02d}-01", "value": str(1000 + m)} for m in range(1, 11)]
    csv_file = make_csv(rows)

    run_pipeline(
        raw_csv=csv_file,
        db_path=pipeline_paths["db_path"],
        schema_path=pipeline_paths["schema_path"],
        report_path=pipeline_paths["report_path"],
        log_path=pipeline_paths["log_path"],
    )

    with sqlite3.connect(pipeline_paths["db_path"]) as conn:
        (count,) = conn.execute("SELECT COUNT(*) FROM gdp_observations").fetchone()

    assert count == 10


# ---------------------------------------------------------------------------
# 3. Exact values persisted -- DB mirrors CSV contents precisely
# ---------------------------------------------------------------------------


def test_db_values_match_input(make_csv, pipeline_paths):
    source_rows = [
        {"date": "2022-01-01", "value": "18872.50"},
        {"date": "2022-04-01", "value": "18932.00"},
        {"date": "2022-07-01", "value": "19015.20"},
        {"date": "2022-10-01", "value": "19100.10"},
    ]
    csv_file = make_csv(source_rows)

    run_pipeline(
        raw_csv=csv_file,
        db_path=pipeline_paths["db_path"],
        schema_path=pipeline_paths["schema_path"],
        report_path=pipeline_paths["report_path"],
        log_path=pipeline_paths["log_path"],
    )

    with sqlite3.connect(pipeline_paths["db_path"]) as conn:
        db_rows = conn.execute(
            "SELECT date, value FROM gdp_observations ORDER BY date"
        ).fetchall()

    assert len(db_rows) == 4
    for (db_date, db_value), src in zip(db_rows, source_rows, strict=True):
        assert db_date == src["date"]
        assert db_value == pytest.approx(float(src["value"]))


# ---------------------------------------------------------------------------
# 4. First row always has NULL growth_rate (no previous observation)
# ---------------------------------------------------------------------------


def test_first_row_growth_rate_is_null(make_csv, pipeline_paths):
    rows = [
        {"date": "2019-01-01", "value": "1000.00"},
        {"date": "2019-04-01", "value": "1010.00"},
        {"date": "2019-07-01", "value": "1020.10"},
    ]
    csv_file = make_csv(rows)

    run_pipeline(
        raw_csv=csv_file,
        db_path=pipeline_paths["db_path"],
        schema_path=pipeline_paths["schema_path"],
        report_path=pipeline_paths["report_path"],
        log_path=pipeline_paths["log_path"],
    )

    with sqlite3.connect(pipeline_paths["db_path"]) as conn:
        row = conn.execute(
            "SELECT growth_rate FROM gdp_observations ORDER BY date LIMIT 1"
        ).fetchone()

    assert row[0] is None, "First row must have NULL growth_rate"


# ---------------------------------------------------------------------------
# 5. Growth rate arithmetic -- known inputs -> verified outputs
#
#    Rows used:
#      2020-01-01: 1000.00  -> growth = NULL          (first row)
#      2020-04-01: 1100.00  -> growth = +10.000 %     (100 / 1000)
#      2020-07-01:  990.00  -> growth = -10.000 %     (-110 / 1100)
# ---------------------------------------------------------------------------


def test_growth_rate_computation(make_csv, pipeline_paths):
    rows = [
        {"date": "2020-01-01", "value": "1000.00"},
        {"date": "2020-04-01", "value": "1100.00"},
        {"date": "2020-07-01", "value": "990.00"},
    ]
    csv_file = make_csv(rows)

    run_pipeline(
        raw_csv=csv_file,
        db_path=pipeline_paths["db_path"],
        schema_path=pipeline_paths["schema_path"],
        report_path=pipeline_paths["report_path"],
        log_path=pipeline_paths["log_path"],
    )

    with sqlite3.connect(pipeline_paths["db_path"]) as conn:
        results = conn.execute(
            "SELECT date, growth_rate FROM gdp_observations ORDER BY date"
        ).fetchall()

    date_to_growth = {r[0]: r[1] for r in results}

    assert date_to_growth["2020-01-01"] is None
    assert date_to_growth["2020-04-01"] == pytest.approx(10.0)
    # (990 - 1100) / 1100 * 100 = -10.0 %
    assert date_to_growth["2020-07-01"] == pytest.approx(-10.0)


# ---------------------------------------------------------------------------
# 6. Report file exists and contains all expected Markdown sections
# ---------------------------------------------------------------------------


def test_report_exists_and_has_sections(make_csv, pipeline_paths):
    rows = [
        {"date": "2021-01-01", "value": "500.00"},
        {"date": "2021-04-01", "value": "510.00"},
    ]
    csv_file = make_csv(rows)

    run_pipeline(
        raw_csv=csv_file,
        db_path=pipeline_paths["db_path"],
        schema_path=pipeline_paths["schema_path"],
        report_path=pipeline_paths["report_path"],
        log_path=pipeline_paths["log_path"],
    )

    report_text = pipeline_paths["report_path"].read_text(encoding="utf-8")

    assert "# Kata 4" in report_text
    assert "Total rows in SQLite" in report_text
    assert "GDP Value Stats" in report_text
    assert "Growth Rate Stats" in report_text


# ---------------------------------------------------------------------------
# 7. Report statistics match what is actually in the database
#
#    4 rows at 1000, 1100, 1210, 1331 (10% compound growth each quarter)
#      - count = 4
#      - min value  = 1000.00,  max = 1331.00,  avg = 1160.25
#      - all growth rates = 10.00 %
# ---------------------------------------------------------------------------


def test_report_statistics_accuracy(make_csv, pipeline_paths):
    rows = [
        {"date": "2023-01-01", "value": "1000.00"},
        {"date": "2023-04-01", "value": "1100.00"},
        {"date": "2023-07-01", "value": "1210.00"},
        {"date": "2023-10-01", "value": "1331.00"},
    ]
    csv_file = make_csv(rows)

    run_pipeline(
        raw_csv=csv_file,
        db_path=pipeline_paths["db_path"],
        schema_path=pipeline_paths["schema_path"],
        report_path=pipeline_paths["report_path"],
        log_path=pipeline_paths["log_path"],
    )

    report = pipeline_paths["report_path"].read_text(encoding="utf-8")

    assert "**4**" in report          # total row count
    assert "**1000.00**" in report    # min value
    assert "**1331.00**" in report    # max value
    assert "**1160.25**" in report    # avg value  (4641 / 4)
    assert "**10.00%**" in report     # growth rate stats (all equal 10 %)


# ---------------------------------------------------------------------------
# 8. Invalid rows (non-numeric value) are silently skipped and logged
# ---------------------------------------------------------------------------


def test_invalid_rows_skipped_and_logged(make_csv, pipeline_paths):
    rows = [
        {"date": "2020-01-01", "value": "1000.00"},
        {"date": "2020-04-01", "value": "N/A"},        # invalid
        {"date": "2020-07-01", "value": "not a num"},  # invalid
        {"date": "2020-10-01", "value": "1100.00"},
    ]
    csv_file = make_csv(rows)

    run_pipeline(
        raw_csv=csv_file,
        db_path=pipeline_paths["db_path"],
        schema_path=pipeline_paths["schema_path"],
        report_path=pipeline_paths["report_path"],
        log_path=pipeline_paths["log_path"],
    )

    with sqlite3.connect(pipeline_paths["db_path"]) as conn:
        (count,) = conn.execute("SELECT COUNT(*) FROM gdp_observations").fetchone()

    assert count == 2, "Only the 2 valid rows should be in the database"

    log_text = pipeline_paths["log_path"].read_text(encoding="utf-8")
    assert log_text.count("[INVALID]") == 2
    assert "N/A" in log_text
    assert "not a num" in log_text


# ---------------------------------------------------------------------------
# 9. Rows with a missing / empty date field are also rejected and logged
# ---------------------------------------------------------------------------


def test_missing_date_rows_logged(make_csv, pipeline_paths):
    rows = [
        {"date": "2020-01-01", "value": "1000.00"},
        {"date": "",           "value": "9999.00"},  # missing date
        {"date": "2020-07-01", "value": "1020.00"},
    ]
    csv_file = make_csv(rows)

    run_pipeline(
        raw_csv=csv_file,
        db_path=pipeline_paths["db_path"],
        schema_path=pipeline_paths["schema_path"],
        report_path=pipeline_paths["report_path"],
        log_path=pipeline_paths["log_path"],
    )

    with sqlite3.connect(pipeline_paths["db_path"]) as conn:
        (count,) = conn.execute("SELECT COUNT(*) FROM gdp_observations").fetchone()

    assert count == 2, "Row with empty date must be excluded"

    log_text = pipeline_paths["log_path"].read_text(encoding="utf-8")
    assert "[INVALID]" in log_text
    assert "missing date" in log_text


# ---------------------------------------------------------------------------
# 10. Idempotency -- running the pipeline twice on the same CSV does NOT
#     duplicate rows (INSERT OR REPLACE on PRIMARY KEY)
# ---------------------------------------------------------------------------


def test_idempotent_pipeline(make_csv, pipeline_paths):
    rows = [
        {"date": "2020-01-01", "value": "1000.00"},
        {"date": "2020-04-01", "value": "1010.00"},
        {"date": "2020-07-01", "value": "1020.10"},
    ]
    csv_file = make_csv(rows)

    kwargs = {
        "raw_csv": csv_file,
        "db_path": pipeline_paths["db_path"],
        "schema_path": pipeline_paths["schema_path"],
        "report_path": pipeline_paths["report_path"],
        "log_path": pipeline_paths["log_path"],
    }

    run_pipeline(**kwargs)
    run_pipeline(**kwargs)  # second run -- must not duplicate

    with sqlite3.connect(pipeline_paths["db_path"]) as conn:
        (count,) = conn.execute("SELECT COUNT(*) FROM gdp_observations").fetchone()

    assert count == 3, "Idempotent load must not create duplicate rows"


# ---------------------------------------------------------------------------
# 11. Dry-run -- no database, report, or log file should be created
# ---------------------------------------------------------------------------


def test_dry_run_writes_nothing(make_csv, pipeline_paths):
    rows = [
        {"date": "2020-01-01", "value": "1000.00"},
        {"date": "2020-04-01", "value": "1010.00"},
    ]
    csv_file = make_csv(rows)

    exit_code = run_pipeline(
        raw_csv=csv_file,
        db_path=pipeline_paths["db_path"],
        schema_path=pipeline_paths["schema_path"],
        report_path=pipeline_paths["report_path"],
        log_path=pipeline_paths["log_path"],
        dry_run=True,
    )

    assert exit_code == 0
    assert not pipeline_paths["db_path"].exists(), (
        "dry_run must not create the database"
    )
    assert not pipeline_paths["report_path"].exists(), (
        "dry_run must not create the report"
    )
    assert not pipeline_paths["log_path"].exists(), (
        "dry_run must not create the log"
    )


# ---------------------------------------------------------------------------
# 12. Large-volume test -- 1 000 rows load correctly and all growth rates
#     are computed (every row except the first has a non-NULL growth_rate)
# ---------------------------------------------------------------------------


def test_large_volume_1000_rows(make_csv, pipeline_paths):
    rows = make_quarterly_rows(1000, start_value=243.1)
    csv_file = make_csv(rows)

    run_pipeline(
        raw_csv=csv_file,
        db_path=pipeline_paths["db_path"],
        schema_path=pipeline_paths["schema_path"],
        report_path=pipeline_paths["report_path"],
        log_path=pipeline_paths["log_path"],
    )

    with sqlite3.connect(pipeline_paths["db_path"]) as conn:
        (total,) = conn.execute("SELECT COUNT(*) FROM gdp_observations").fetchone()
        (nulls,) = conn.execute(
            "SELECT COUNT(*) FROM gdp_observations WHERE growth_rate IS NULL"
        ).fetchone()
        (non_nulls,) = conn.execute(
            "SELECT COUNT(*) FROM gdp_observations WHERE growth_rate IS NOT NULL"
        ).fetchone()

    assert total == 1000,    f"Expected 1 000 rows loaded, got {total}"
    assert nulls == 1,       "Exactly one row (the first) must have NULL growth_rate"
    assert non_nulls == 999, "All 999 subsequent rows must have computed growth_rates"

    # Sanity-check the report was also generated for 1 000 rows
    report = pipeline_paths["report_path"].read_text(encoding="utf-8")
    assert "**1000**" in report
