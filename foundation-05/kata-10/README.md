# Kata 10 - Test-Driven Development

**Course:** CIDM 6330 — Software Systems Development  
**Student:** Francis Kelechi Njoku  
**Focus:** TDD practice + git stash / worktree  

---

## What This Kata Does

Kata 10 adds a GDP Analysis module (`analysis.py`) to the Kata 4/9 pipeline
using strict TDD: **test first, implement second, refactor third**.

The feature set — contraction detection, peak/trough identification, and a
summary report — was built across **three complete RED-GREEN-REFACTOR cycles**,
each represented by three consecutive commits in the git history.

---

## Repository Layout

```
kata-10/
├── analysis.py          ← Feature module (built cycle-by-cycle)
├── tests/
│   ├── __init__.py
│   ├── conftest.py      ← Known-dataset DB fixture + path helpers
│   └── test_analysis_tdd.py  ← 11 TDD tests + 1 bug-fix test
├── AI_LOG.md
└── README.md
```

---

## Running the Tests

From the **repository root**:

```powershell
python -m pytest foundation-05/kata-10/tests/ -v
```

---

## TDD Cycle Summary

| Cycle | Function | RED | GREEN | REFACTOR |
|-------|----------|-----|-------|----------|
| 1 | `detect_contractions` | ImportError | single SQL query | extract `_CONTRACTIONS_SQL` constant |
| 2 | `compute_peak_trough` | ImportError | two ORDER BY queries | replace namedtuple with `PeakTrough` dataclass |
| 3 | `generate_summary_report` | ImportError | minimal string concat | extract `_contractions_section` helper |
| Bug | `pipeline.generate_report` | TypeError on None | guard on `count == 0` | — |

### Test Inventory

| # | Test | Cycle |
|---|------|-------|
| 1 | `test_detect_contractions_returns_correct_dates` | 1 |
| 2 | `test_detect_contractions_returns_empty_list_when_none` | 1 |
| 3 | `test_detect_contractions_result_is_sorted` | 1 |
| 4 | `test_compute_peak_trough_peak_values` | 2 |
| 5 | `test_compute_peak_trough_trough_values` | 2 |
| 6 | `test_compute_peak_trough_peak_above_trough` | 2 |
| 7 | `test_generate_summary_report_creates_file` | 3 |
| 8 | `test_generate_summary_report_contains_required_sections` | 3 |
| 9 | `test_generate_summary_report_contraction_dates_in_report` | 3 |
| 10 | `test_generate_summary_report_peak_trough_values_in_report` | 3 |
| 11 | `test_generate_report_does_not_crash_on_empty_database` | Bug fix |

---

## Git Stash Practice

During Cycle 2, the Cycle 2 RED tests were partially written when a
context switch was needed to make an unrelated housekeeping commit.

Steps performed:

```bash
# 1. Save WIP to the stash
git stash push -m "WIP: RED tests for compute_peak_trough"

# 2. Make the unrelated commit
git add foundation-05/kata-10/analysis.py
git commit -m "chore(k10): add stash-practice note to analysis module"

# 3. Restore WIP from the stash
git stash pop
```

The stash entry name `WIP: RED tests for compute_peak_trough` made it clear
what was stashed, which is especially helpful when multiple stash entries
exist simultaneously.

---

## Git History Shape

The commit log shows the TDD rhythm clearly:

```
test(k10): [RED]      Cycle 1 - detect_contractions fails
feat(k10): [GREEN]    Cycle 1 - detect_contractions passes
refactor(k10): [REFACTOR]  Cycle 1 - extract SQL constant

chore(k10): stash-practice note (committed while Cycle 2 tests were stashed)

test(k10): [RED]      Cycle 2 - compute_peak_trough fails
feat(k10): [GREEN]    Cycle 2 - compute_peak_trough passes
refactor(k10): [REFACTOR]  Cycle 2 - PeakTrough dataclass

test(k10): [RED]      Cycle 3 - generate_summary_report fails
feat(k10): [GREEN]    Cycle 3 - generate_summary_report passes
refactor(k10): [REFACTOR]  Cycle 3 - extract _contractions_section

test(k10): [RED]      bug-fix - generate_report crashes on empty DB
fix(k9):   [GREEN]    bug-fix - handle zero-row database
```
