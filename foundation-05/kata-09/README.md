# Kata 9 — Integration Testing

**Course:** CIDM 6330 — Software Systems Development  
**Student:** Francis Kelechi Njoku  
**Focus:** Integration testing of the Kata 4 GDP data pipeline  

---

## What This Kata Does

Kata 9 builds a comprehensive integration test suite around the GDP data
pipeline introduced in Kata 4.  The tests exercise the *complete* data flow:

```
raw_gdp.csv  →  validate & transform  →  SQLite database  →  Markdown report
```

Unlike unit tests (which mock or stub individual functions), these tests
run every pipeline stage against real files and a real SQLite database
inside pytest's isolated `tmp_path` directories.

---

## Repository Layout

```
kata-09/
├── pipeline.py          ← Kata 4 pipeline (source under test)
├── schema.sql           ← Database schema
├── data/
│   └── raw_gdp.csv      ← Sample 4-row dataset for manual runs
├── output/              ← Created at runtime; ignored by git
├── tests/
│   ├── __init__.py
│   ├── conftest.py      ← Shared fixtures (make_csv, pipeline_paths, …)
│   └── test_pipeline_integration.py  ← 12 integration tests
├── AI_LOG.md            ← AI collaboration log (required by instructor)
└── README.md            ← This file
```

---

## Running the Tests

From the **repository root** (where `pyproject.toml` lives):

```bash
# Install pytest if not already present
pip install pytest

# Run all Kata 9 tests
pytest foundation-05/kata-09/tests/ -v

# Run a single test by name
pytest foundation-05/kata-09/tests/ -v -k test_large_volume_1000_rows
```

All 12 tests should pass.  Each test creates its own temporary directory
that pytest cleans up automatically — no manual teardown required.

---

## Test Inventory

| # | Test Name | What It Verifies |
|---|-----------|-----------------|
| 1 | `test_full_pipeline_smoke` | Happy path: pipeline exits 0, DB and report created |
| 2 | `test_exact_row_count_loaded` | DB row count == CSV input row count |
| 3 | `test_db_values_match_input` | DB values are byte-for-byte equal to CSV values |
| 4 | `test_first_row_growth_rate_is_null` | First observation has NULL growth_rate |
| 5 | `test_growth_rate_computation` | Known inputs produce known growth percentages |
| 6 | `test_report_exists_and_has_sections` | Report contains all required Markdown sections |
| 7 | `test_report_statistics_accuracy` | Report numbers match database aggregates exactly |
| 8 | `test_invalid_rows_skipped_and_logged` | Non-numeric values rejected and logged |
| 9 | `test_missing_date_rows_logged` | Empty-date rows rejected and logged |
| 10 | `test_idempotent_pipeline` | Running twice yields no duplicate rows |
| 11 | `test_dry_run_writes_nothing` | `--dry-run` creates no files at all |
| 12 | `test_large_volume_1000_rows` | 1 000-row load succeeds; all growth rates computed |

---

## Git Reflog Recovery (documented)

As required by the Kata 9 Git task, the reflog recovery workflow was
performed on this branch.  A summary of the steps:

1. Made three commits with the initial pipeline and schema files.
2. Simulated an accident: `git reset --hard HEAD~3`
3. Confirmed the commits appeared "lost" (`git log --oneline` showed them gone).
4. Ran `git reflog` to find the SHA of the lost HEAD.
5. Restored with `git reset --hard <sha>`.
6. Verified all files returned intact.

See `AI_LOG.md` for the full session notes.

---

## CI

A GitHub Actions workflow at `.github/workflows/integration-tests.yml`
runs these tests automatically on every push and pull request that touches
`foundation-05/kata-09/**`.
