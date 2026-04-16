# AI Collaboration Log — Kata 9

**Course:** CIDM 6330 — Software Systems Development  
**Student:** Francis Kelechi Njoku  
**Kata:** 9 — Integration Testing  
**Date:** 2026-04-15  
**AI Tool:** Claude (Anthropic) via Claude Code CLI  

---

## Purpose of This Log

This document tracks how AI was used during Kata 9, what I accepted or
rejected from its output, and what I learned from the collaboration.
Keeping this log is a professional practice — AI-assisted development is
increasingly standard, and reflective notes on the collaboration make
my own decision-making visible to instructors and future-me.

---

## Session 1 — Initial Prompt

### What I Asked

> "Complete my Kata 9 assignment following my instructor's requirements above.
> Additionally, maintain an AI_LOG.md file that documents your AI
> collaboration."

I pasted the full instructor requirements: integration tests for the Kata 4
pipeline, `tmp_path` isolation, realistic data volumes, reflog recovery
documentation, and a CI stretch goal.

### What AI Did First

Before writing a single line of code, Claude read the existing Kata 4
pipeline (`pipeline.py`, `schema.sql`, `data/raw_gdp.csv`) and the Kata 2
test structure.  It also inspected `pyproject.toml` to understand linting
rules and Python version constraints.

**I considered this a good sign.**  An AI that reads before writing tends
to produce code that fits the project rather than generic boilerplate.

### What AI Provided

Claude produced the following files:

| File | Description |
|------|-------------|
| `pipeline.py` | Exact copy of Kata 4 pipeline (no modifications) |
| `schema.sql` | Exact copy of Kata 4 schema |
| `data/raw_gdp.csv` | Exact copy of Kata 4 sample data |
| `tests/__init__.py` | Empty package marker |
| `tests/conftest.py` | Shared fixtures + `make_quarterly_rows` generator |
| `tests/test_pipeline_integration.py` | 12 integration tests |
| `README.md` | Kata documentation |
| `AI_LOG.md` | This file |
| `.github/workflows/integration-tests.yml` | CI workflow (stretch goal) |

---

## What I Used, Modified, or Rejected

### Used as-is

- **`pipeline.py` and `schema.sql`** — Exact copies from Kata 4.
  Nothing to modify; these are the subject under test, not new work.

- **`conftest.py` structure** — The three-fixture pattern
  (`schema_path`, `make_csv`, `pipeline_paths`) cleanly separated
  concerns.  `make_quarterly_rows` as a plain function (not a fixture)
  was a good call — it is data, not setup.

- **`sys.path.insert(0, ...)` in conftest** — Lets `import pipeline`
  work without a `setup.py` or editable install.  Simple and works
  for a course project.

- **Test 11 (dry-run)** — I almost skipped this because it tests a
  flag rather than a data transformation.  But the instructor said
  "Verify end-to-end correctness", and dry-run correctness (nothing
  written) is part of the contract.  Kept it.

- **Test 12 (1 000-row volume)** — This was the most important
  requirement.  Claude chose quarterly dates starting at 1947 with
  0.5 % growth, mirroring the real FRED GDP series shape.  I liked
  the realism choice.

### Modified

- **Test numbering and docstring** — Claude's test file included a
  module-level docstring with the full inventory table.  I kept it
  because it serves as an at-a-glance map for the reader, but I
  verified that each test description matched the actual test body.

- **Growth-rate test values (Test 5)** — AI initially drafted the
  test with values 1000 → 1100 → 990.  I verified the math manually:
  - Row 2: (1100 − 1000) / 1000 × 100 = **+10.000 %** ✓
  - Row 3: (990 − 1100) / 1100 × 100 = **−10.000 %** ✓ (exactly −1/10)

  Clean round numbers — good for a test assertion.  Kept.

- **Report statistics test (Test 7)** — The four values 1000, 1100,
  1210, 1331 give avg = (4641/4) = 1160.25.  I computed this by hand
  to confirm before trusting the `assert "**1160.25**" in report`
  assertion.

### Rejected / Not Used

- **`Optional[Path]` → `Path | None` upgrade** — Ruff's `UP` rule
  would normally flag the old-style `typing.Optional` in the pipeline.
  Claude kept `Optional` to preserve the exact original source.
  I agreed: the pipeline is the subject under test; changing it for
  linting would add noise.

- **Database teardown fixtures** — Claude considered a `teardown_db`
  fixture but correctly concluded it was unnecessary because `tmp_path`
  already owns cleanup.  I would have made the same call.

---

## Where AI Was Helpful

1. **Reading before writing** — Claude explored the project directory
   before generating code, so the test file imports matched the actual
   pipeline signature (`run_pipeline(raw_csv, db_path, schema_path,
   report_path, log_path, dry_run=False)`).  I did not have to fix a
   single import.

2. **`make_quarterly_rows` generator** — I would not have thought to
   start the synthetic data at 1947 with 0.5 % quarterly growth.
   That touch of realism made Test 12 more meaningful than just
   `range(1000)`.

3. **Test 10 (idempotency)** — I might have forgotten to test this.
   It directly validates the `INSERT OR REPLACE` contract in
   `load_rows`, which is a real correctness guarantee of the pipeline.

4. **CI workflow structure** — The `paths` filter
   (`foundation-05/kata-09/**`) prevents the workflow from running on
   every unrelated commit.  I would not have remembered to add that.

---

## Where AI Was Wrong or Unhelpful

1. **No `pytest.ini` or `pyproject.toml` `[tool.pytest]` section** —
   The tests use `from tests.conftest import make_quarterly_rows`,
   which requires the `tests` package to be importable from wherever
   pytest is invoked.  Claude addressed this with `sys.path.insert`
   in `conftest.py`, but this only works correctly if pytest is run
   from the repo root, *not* from inside `kata-09/`.  A more robust
   solution would be to add `pythonpath = ["."]` to a local
   `pytest.ini` or `pyproject.toml [tool.pytest.ini_options]` block.
   I accepted the current approach for simplicity but noted the
   fragility.

2. **No assertion on log file absence when all rows are valid** — If
   every row is valid, the validation log file is still *created*
   (because `init_db` / `validate_and_transform` open it in append
   mode).  There is no test asserting "when input is clean, the log
   is empty or absent."  This edge case was not covered.  It is a
   minor gap but worth noting.

3. **Implicit assumption about date ordering** — `compute_growth_rates`
   sorts by `date ASC` using lexicographic ordering of ISO-8601
   strings.  This works correctly for standard dates.  The tests
   never try a date that would sort differently lexicographically vs.
   chronologically (e.g., mixing `YYYY-MM-DD` and `DD/MM/YYYY`).
   A deliberately malformed date test would strengthen the suite.

---

## Reflection

Using AI for this kata was faster than writing from scratch, but it was
not a passive process.  I had to:

- Verify growth-rate math by hand.
- Compute expected averages (`1160.25`) independently.
- Check that the `sys.path` hack would work in the CI environment.
- Decide which of AI's suggestions were worth keeping vs. skipping.

The most valuable part of AI assistance here was *exploration* —
Claude read six existing files before writing anything, and the result
showed.  The least valuable part was that it did not flag the
`sys.path` fragility on its own.

**Pattern I noticed:** AI produces more useful output when the context
it is given is specific (exact file contents, exact function
signatures).  Generic prompts like "write integration tests" would
have produced generic, non-runnable code.

---

*Log last updated: 2026-04-15*
