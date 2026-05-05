# Drift Consultation Log — Foundation 4: Deliver
**Student:** Francis Kelechi Njoku
**Course:** CIDM 6330 — Software Architecture, Spring 2026
**Foundation Theme:** Deliver — complete MVP, practice TDD, document AI process, write ADRs

---

## Simulated Consultation Transcript

---

**Instructor:** Foundation 4 is the Deliver phase. What does "deliver" mean to you in this context, and how did kata-09 and kata-10 together serve that?

**Student:** Deliver means the work is ready to be handed off — it is tested, it is documented, and the decisions behind it are defensible. Kata-09 completed the pipeline that had been evolving since Foundation 2. Kata-10 added an analysis layer on top of that pipeline using strict TDD and demonstrated that new features can be added without breaking existing behavior. Together they show not just a working artifact but a working process: the pipeline is correct by test, not just by inspection.

---

**Instructor:** Foundation 4 also included kata-07 and kata-08. Where do those fit in the Deliver story?

**Student:** Kata-07 was unit testing — writing isolated tests for individual functions without depending on the database or the filesystem. That discipline is what made kata-09 and kata-10 trustworthy: by the time I was doing TDD in kata-10, writing tests first was already a practiced habit, not a new skill. Kata-08 introduced test doubles — mocks and stubs — which let me test functions that call external systems without actually calling them. The specific lesson was knowing when a test double is appropriate versus when it hides real behavior. For the pipeline I avoided mocking the database because a real SQLite in-memory database is fast, simple, and tests the actual SQL. I only used doubles where the external call — like a network request — was genuinely outside the test boundary. Kata-07 and kata-08 were submitted via their own separate PRs; kata-09 and kata-10 are the delivery phase where those testing skills were applied end-to-end.

---

**Instructor:** Kata-09 is essentially the final form of the pipeline from kata-04. What changed between kata-04 and kata-09?

**Student:** The core structure stayed the same — extract, validate, load, compute growth rates, report — but kata-09 consolidated and hardened it. The `generate_report` function in kata-09 is more defensive: it handles the case where the database is empty rather than crashing on `None` values when there is no data. The argument handling is more explicit, and the dry-run path is cleaner. Kata-04 was the sketch; kata-09 is the version I would actually hand to someone else to run.

---

**Instructor:** In kata-10, why contraction detection rather than rolling averages or year-over-year growth?

**Student:** I evaluated all three options against one criterion: do the TDD cycles stay genuinely independent? Rolling averages require adding a new column to the schema first, so the test for computing the average depends on the test for storing it — the cycles would be tangled. Year-over-year growth depends on having exactly four prior quarters of data in the test fixtures, which creates brittle test data. Contraction detection, peak/trough identification, and summary report are genuinely orthogonal: each queries the existing table in a different way, and the tests for each can be written without any dependency on the others passing first.

---

**Instructor:** Walk me through one full TDD cycle from kata-10 — RED, GREEN, REFACTOR.

**Student:** I will use Cycle 1, `detect_contractions`. RED: I wrote three tests first — one asserting that two contractions are returned in date order for a known dataset, one asserting that an empty list is returned when there are no negative growth rates, and one asserting that rows with `None` growth rate are excluded. All three failed because the function did not exist yet. GREEN: I wrote the minimal implementation — a single SQL query selecting dates where `growth_rate < 0` ordered by date, returning them as a plain list. All three tests passed. REFACTOR: I extracted the SQL string to a module-level constant so it could be read in one place, and added a docstring describing the empty-list contract. No new tests — refactor must not change behavior, only clarity.

---

**Instructor:** The test data uses values like 1000, 1100, 990, 1188. Why those specific numbers?

**Student:** I asked AI to generate a six-row dataset where all growth rates are exact multiples of 10% or 20%. The reason is that floating-point arithmetic on arbitrary values often produces results like -10.000000000001 instead of -10.0, which causes assert statements to fail even when the logic is correct. With clean multiples I could write `assert growth == -10.0` without needing `pytest.approx`. I manually verified every calculation in the AI log to confirm the math held before using the dataset.

---

**Instructor:** The `PeakTrough` dataclass uses `frozen=True`. You also used `frozen=True` on `GdpRow` in the pipeline. Is that a coincidence?

**Student:** No. `GdpRow` uses `frozen=True` in `pipeline.py` because a row read from a source should not change after it is created. When I designed `PeakTrough` I applied the same reasoning: peak and trough are computed results derived from the database state at a point in time. Once computed they should not be mutated. Consistency in the codebase also matters — a reader who sees `frozen=True` in one dataclass and expects it elsewhere will find it. I called that out explicitly in the AI log.

---

**Instructor:** The bug fix in kata-10 addressed `generate_report` crashing on an empty database. How did you find that bug?

**Student:** AI identified it. The `generate_report` function calls `f"{min_v:.2f}"` where `min_v` comes from `SELECT MIN(value) FROM gdp_observations`. When the table is empty, SQLite returns `NULL` for aggregate functions, which Python receives as `None`. Formatting `None` with `:.2f` raises `TypeError`. I confirmed the bug by running the failing test and seeing the exact traceback before writing the fix.

---

**Instructor:** AI suggested `if min_v is None` as the guard. You used `if count == 0 or min_v is None`. Why add the count check?

**Student:** Because `count == 0` expresses the intent more directly. A reader immediately understands "zero rows means no data." The `min_v is None` guard requires knowing that SQLite aggregates return NULL on empty tables — that is a SQL-specific detail, not obvious from the Python. I kept both conditions because `min_v is None` catches a theoretical edge case where count is nonzero but the aggregate still returns NULL, which should not happen given the schema constraints but costs nothing to guard against.

---

**Instructor:** You practiced `git stash` in kata-10. What is stash actually solving?

**Student:** Stash solves the context-switching problem. Mid-cycle I had RED tests in my working tree that could not be committed — they were failing by design. But I needed to make an unrelated housekeeping commit on the same branch. Without stash, I would have to either commit broken tests or discard them. Stash saves the working-tree state, lets me make the clean commit, and then restores the tests with `git stash pop`. The key insight is that stash is not a backup mechanism — it is a temporary shelf for work in progress so you can shift context without losing state.

---

**Instructor:** What did you learn about working with AI across all four foundations that you did not know at the start?

**Student:** At the start I treated AI as a code generator — ask a question, get code, use it. By Foundation 4 I was using AI differently: for option analysis first, code generation second. The most valuable contribution in kata-10 was AI pointing out that rolling averages would tangle the TDD cycles — that was an architectural insight, not code. I would have discovered the tangle only after wasting time implementing the wrong feature. Asking AI "what are the trade-offs of these four options?" before asking "write this function" consistently produced better results than going straight to implementation.

---

**Instructor:** If I asked you to add a new feature to the analysis module right now, how confident are you that your tests would catch regressions?

**Student:** Confident for the functions that are tested, less confident for edge cases that are not covered. The current tests verify the happy path and the empty-database path for each function. They do not cover, for example, a database with exactly one row — where `detect_contractions` should return an empty list because there is no previous row to compare against. That gap exists and I know it exists. If I were adding a feature, I would write tests for those boundary cases first before touching the implementation, following the same RED-GREEN-REFACTOR discipline.

---

*Log completed: 2026-05-05*
*Foundation: 4 — Deliver*
*Katas covered: kata-09 (complete pipeline, hardening), kata-10 (TDD — 3 cycles + bug fix, git stash, PeakTrough dataclass, detect_contractions, compute_peak_trough, generate_summary_report)*
