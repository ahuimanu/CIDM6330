# Architecture Reality Check — Foundation 3

## Style Validation

**Selected style:** Pipeline Architecture (Pipes and Filters), as defined in Foundation 2.

**Does it still fit?** Yes — and implementation confirmed why.

The core problem is a linear mathematical equation: `pct_change → rolling mean → S_score → Recommendation`. Building it made this even more obvious. Every component hands a Pandas DataFrame to the next with a clearly defined shape. There were zero moments where I needed a feedback loop, a shared state store, or parallel fan-out. The pipeline shape matched the problem shape exactly.

**What implementation revealed that design didn't:**

- The `transform.py` module ended up doing the work of three Foundation 2 components (Normalization, Aggregation, Calculation) in a single file. In design, these felt like separate filters. In practice, they are three sequential operations on the same DataFrame — splitting them into separate files would have added import complexity with no testability benefit. I consolidated them deliberately.
- The Foundation 1 `FRED_helper.py` became an implicit dependency of the Ingestion component. The boundary between Foundation 1 (helper) and Foundation 3 (acquire) is clean at the import level but not obvious from the folder structure. This is a documentation risk, not a design flaw.

---

## Characteristic Assessment

### Auditability
**Achieving it? Partially.**

The pipeline writes `combined.csv` (raw ingested values), `transformed.json` (intermediate rolling metrics + S_score + Recommendation), and `pipeline.log` (timestamped run log). A reviewer can open these three files and reconstruct exactly what the system saw on any run.

**Harder than expected:** Point-in-time FRED data is not cached. If FRED revises a historical series value (which they do), re-running the pipeline with the same date range will produce slightly different raw numbers. True auditability requires archiving the raw FRED JSON response at acquisition time, not just the derived CSV. This is not yet implemented.

**Trade-off made:** Accepted partial auditability (intermediate artifacts logged) over full provenance (immutable FRED response archive) to keep the MVP scope manageable.

### Data Integrity
**Achieving it? Yes.**

The `pct_change()` → `rolling(3).mean()` chain enforces unit normalization before the S_score calculation runs. If a series fails to fetch, `acquire.py` logs an error and the pipeline aborts rather than proceeding with partial data. Unit tests assert the exact numeric output of the transformation, which catches silent regressions.

**Harder than expected:** NaN handling. `pct_change()` produces NaN for the first row; `rolling(3).mean()` produces NaN for the first two rows after that. The `dropna(how="all")` calls handle this, but "drop all-NaN rows" is different from "drop any-NaN rows." If only one series is missing a month, the row is kept with a NaN in that column — the S_score will still compute (pandas ignores NaN in `mean(axis=1)` by default). This is the correct behavior but was not explicitly tested.

**Trade-off made:** Accepted "partial row" handling (compute S_score from available series) over "strict completeness" (abort on any NaN) because FRED series have different update cadences. Strict completeness would make the final month's row permanently unavailable.

### Testability
**Achieving it? Yes — this was the strongest result.**

All three test files (`test_acquire.py`, `test_transform.py`, `test_transform_weights.py`) run in under 1 second with no network calls. The monkeypatch pattern for `get_fred_series` in `test_acquire.py` proved that the acquisition layer is fully injectable. The transformation tests assert exact floating-point values, not just "something was returned."

**Harder than expected:** Monkeypatching required targeting the correct namespace (`Foundation3.acquire.get_fred_series`, not `Foundation1.FRED_helper.get_fred_series`). This is a Python import mechanics subtlety — the name must be patched where it is *used*, not where it is *defined*. This caused a test failure that was only caught because tests were actually run.

---

## Component Evolution

| Foundation 2 Component | Foundation 3 Reality | Change |
|---|---|---|
| Ingestion Component | `Foundation3/acquire.py` | Matches design; added retry logic not in original spec |
| Normalization Component | `Foundation3/transform.py` (lines 30–31) | Merged into transform module |
| Aggregation Component | `Foundation3/transform.py` (lines 33–34) | Merged into transform module |
| Calculation Component | `Foundation3/transform.py` (lines 38–57) | Merged into transform module |
| Enrichment & Output | `Foundation3/pipeline.py` + `transform.py` | Split: transform adds Recommendation, pipeline writes JSON |

The three middle components (Normalization, Aggregation, Calculation) collapsed into a single module. This was the right call: they share state (the same DataFrame), have no independent testability benefit as separate files, and the Pipeline architecture does not require physical file separation — only logical sequential ordering.

---

## What I Would Do Differently

1. **Archive raw FRED responses at acquisition time.** Writing the raw JSON payload from FRED (before any parsing) to a timestamped file would provide true point-in-time auditability. The current approach logs derived CSVs, which are already post-parse.

2. **Make the S_score weighting formula explicit.** The Foundation 2 component spec defines `S = w1(ΔIP) + w2(ΔCapUtil) - w3(ΔPPI) + w4(ΔInv)` — note the **negative weight on PPI** (rising prices are a bad signal). The current `transform.py` uses equal positive weights on all four series, which treats rising prices as a *good* supply signal. The weights dict parameter exists but no default reflects the intended formula. I would set asymmetric defaults that match the stated equation.

3. **Add a validation filter before the S_score calculation.** Foundation 2 explicitly called for a "Validation Filter" gatekeeper that asserts all inputs are in percentage form before the calculation runs. Currently there is no such assertion — the pipeline trusts that `pct_change()` succeeded. A simple `assert (df.abs() < 5).all().all()` (no series moved 500% in a month) would catch data corruption early.
