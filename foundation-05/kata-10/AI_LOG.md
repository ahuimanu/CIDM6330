# AI Collaboration Log - Kata 10 (Test-Driven Development)

## Context

This assignment required implementing a new feature using strict TDD (test
first, implement second, refactor third) and practicing git stash.  I chose
to add a GDP Analysis module that extends the Kata 4/9 pipeline with
contraction detection, peak/trough identification, and a summary report.

## AI Tools Used

- Claude (Anthropic) via Claude Code CLI

---

## Interaction 1 - Choosing a Feature

**What I asked:**
What feature could I add to the existing GDP pipeline that would produce
three natural TDD cycles with meaningfully different tests?

**What AI provided:**
Four options: rolling average, CSV export, contraction detection, and
year-over-year growth.  For each it explained how many TDD cycles it would
naturally break into.

**What I used:**
Contraction detection + peak/trough + summary report.  The three functions
are genuinely independent, each testable with a single known dataset, and the
progression from a query to a computation to a report mirrors the pipeline's
own architecture.

**What I rejected:**
Rolling average.  It requires schema changes (adding a column) and would have
tangled the TDD cycles together — the test for storing averages would depend
on the test for computing them before the computation even existed.

---

## Interaction 2 - Test Data Design

**What I asked:**
What test data values would let me assert exact growth rates without
floating-point surprises?

**What AI provided:**
A six-row dataset where all growth rates are exact multiples of 10%:
1000 → 1100 (+10%), → 990 (-10%), → 1188 (+20%), → 1069.2 (-10%),
→ 1176.12 (+10%).

**What I used:**
Exactly this dataset.  I manually verified each growth rate:
- (990 - 1100) / 1100 * 100 = -10.0 ✓
- (1188 - 990) / 990 * 100 = +20.0 ✓
- (1069.2 - 1188) / 1188 * 100 = -10.0 ✓
- (1176.12 - 1069.2) / 1069.2 * 100 = +10.0 ✓

**What I modified:**
Nothing — the math held up.

---

## Interaction 3 - Cycle 1 GREEN (detect_contractions)

**What I asked:**
Write the minimal implementation to pass the three Cycle 1 tests.

**What AI provided:**
```python
def detect_contractions(db_path: Path) -> list[str]:
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            "SELECT date FROM gdp_observations WHERE growth_rate < 0 ORDER BY date"
        ).fetchall()
    return [r[0] for r in rows]
```

**What I used:**
This exactly.  It is the simplest possible implementation that passes all
three tests.  The `ORDER BY date` clause satisfies the sort test without any
Python-side sorting.

**What I rejected:**
An alternative that fetched all rows and filtered in Python.  That would have
been slower and less expressive.

---

## Interaction 4 - Cycle 1 REFACTOR

**What I asked:**
What single refactor would add the most clarity without over-engineering?

**What AI provided:**
Extract the SQL string to a module-level constant and add a docstring
describing the empty-list contract.

**What I used:**
Both suggestions.  The constant means the SQL can be read in one place and
the docstring makes the "empty list = no contractions OR fewer than two rows"
contract explicit for future readers.

**What I rejected:**
A suggestion to add logging.  This is a query function, not a pipeline step
— logging would be noise.

---

## Interaction 5 - Stash Practice

**What I asked:**
How do I demonstrate the stash workflow in a way that is visible in the git
history without faking it?

**What AI provided:**
A concrete sequence: write the RED tests, stash them, make an unrelated
housekeeping commit, then pop the stash.  This way the stash shows up in
`git reflog` and the commit message references it.

**What I used:**
This approach exactly.  The housekeeping commit added a comment to
`analysis.py`; the stash note was "WIP: RED tests for compute_peak_trough".

**Why it worked:**
The commit message for the RED state explicitly says the tests were stashed
and then restored, so the git history is self-documenting without needing a
screenshot.

---

## Interaction 6 - Cycle 2 REFACTOR (namedtuple vs dataclass)

**What I asked:**
The GREEN implementation used a namedtuple created inside the function.
Should I refactor to a dataclass?

**What AI provided:**
Yes, with three reasons: (1) the field types are declared explicitly, (2) the
return type annotation becomes concrete instead of `Any`, (3) the import moves
out of the function body to the module level.

**What I used:**
The `@dataclass(frozen=True)` approach.  `frozen=True` mirrors the
`@dataclass(frozen=True)` pattern already used in `pipeline.py`'s `GdpRow`.
Consistency across the codebase is worth the minor extra line.

---

## Interaction 7 - Bug-Fix TDD

**What I asked:**
What is a real bug in the existing pipeline that I can fix using TDD?

**What AI provided:**
The `generate_report` function in `pipeline.py` calls `f"{min_v:.2f}"` on
values that are `None` when the database is empty, raising `TypeError`.

**What I used:**
This bug exactly.  I confirmed it by running the test before the fix and
seeing the `TypeError: unsupported format string passed to NoneType.__format__`
traceback.

**What I modified:**
The fix was a two-line guard:
```python
if count == 0 or min_v is None:
    md.append("- No data available\n")
else:
    ...
```
AI suggested `if min_v is None` only.  I added `count == 0` as the primary
condition because it is the more readable intent, and `min_v is None` as a
fallback for any edge case where count is nonzero but a value is still None.

---

## Where AI Was Helpful

1. **Feature scoping** — Pointing out that rolling averages require schema
   changes and would tangle the TDD cycles was the most valuable input.
   I would have discovered this only after wasting time.

2. **Exact test data** — Generating six rows with all-clean 10%/20% growth
   rates saved me from trial-and-error arithmetic.

3. **Bug identification** — I would not have thought to look at
   `generate_report`'s empty-database behaviour.  The bug is subtle because
   it only triggers in a state (empty table) that the normal pipeline never
   produces.

---

## Where AI Was Wrong or Unhelpful

1. **Suggesting logging in a query function** — This was unnecessary noise
   for a data-access function and was rejected without discussion.

2. **Suggesting `if min_v is None` as the only guard** — Technically correct
   but less readable than `if count == 0`.  A human reader understands "zero
   rows → no data" immediately; `if min_v is None` requires knowing that
   SQLite aggregates return NULL on empty tables.

3. **No mention of ruff compliance** — The initial GREEN implementation for
   Cycle 2 used a namedtuple created inside the function body with an inline
   `from collections import namedtuple`.  Ruff's `PLC0415` rule flags imports
   inside functions.  AI did not flag this; I caught it during the REFACTOR
   cycle.

---

## Reflection

TDD with AI assistance is different from TDD alone.  Normally the RED phase
forces you to think hard about the API before writing a single line of
implementation.  With AI, there is a temptation to ask "write the tests and
the implementation" in one shot.

I resisted this by asking for tests first, running them to confirm RED, and
only then asking for the implementation.  The discipline matters: two of the
three RED states caught real design decisions (what should `detect_contractions`
return when there are no contractions? an empty list, not None or raising).

The most valuable AI contribution was not code generation but **option
analysis** — helping me choose which feature to build and why rolling averages
were the wrong choice for this kata.

---

*Log last updated: 2026-04-16*
