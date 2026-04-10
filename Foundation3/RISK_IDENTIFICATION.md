# Risk Identification — Foundation 3

## Technical Risks

### 1. FRED API Key Exposure
**Risk:** `FRED_API_KEY` is read from a `.env` file at the repo root. If `.env` is accidentally committed (e.g., a missing `.gitignore` entry), the key is exposed in git history permanently.  
**Likelihood:** Low — `.env` is in `.gitignore`. But a single misfire destroys it.  
**Mitigation:** The key has a free public FRED account scope (no billing attached), limiting blast radius. Still: never commit `.env`. CI uses a GitHub Actions secret, not a checked-in file.

### 2. Retry Timeout in Acquisition
**Risk:** `acquire.py` uses a `backoff * attempt` sleep between retries (1.5s, 3.0s, 4.5s). With 4 series and 3 retries each, a full network outage could cause the pipeline to hang for ~72 seconds before failing.  
**Likelihood:** Low in normal conditions; higher in CI on a slow runner.  
**Mitigation:** Current behavior is acceptable for a monthly batch job. If converted to an interactive tool, add a hard timeout per request.

### 3. Pandas Version Sensitivity
**Risk:** `pct_change()` and `rolling().mean()` behavior can differ across pandas major versions (e.g., `dropna` default changes in pandas 2.x). Tests pass on the developer's environment but could silently produce different numeric results on a different pandas version.  
**Likelihood:** Medium — `requirements.txt` does not pin a pandas version.  
**Mitigation:** Pin `pandas>=2.0,<3.0` in `requirements.txt`. The existing unit tests assert exact floating-point values, which will catch a version regression immediately.

---

## Data Risks

### 4. FRED Series Retroactive Revisions
**Risk:** FRED revises historical series values after publication (e.g., seasonal adjustment corrections). Re-running the pipeline over a past date range will produce slightly different numbers than a run performed on the original date.  
**Likelihood:** High — FRED revises data regularly.  
**Impact:** Undermines point-in-time auditability. A manager who asks "why did the system say OVERBUY in March?" cannot get the exact same numbers by re-running the pipeline today.  
**Mitigation (not yet implemented):** Archive the raw FRED JSON response payload (including the `vintage_date` field) at acquisition time. This is the largest unresolved architectural risk.

### 5. Series Discontinuation or ID Change
**Risk:** FRED periodically deprecates series or changes their identifiers. If `IPG3344S` is renamed or discontinued, `acquire.py` will log an error and the pipeline will abort with no output.  
**Likelihood:** Low for established BLS/Fed series, but non-zero over a multi-year horizon.  
**Impact:** Silent data gap — the pipeline fails loudly (good), but there's no automated alert.  
**Mitigation:** The retry logic and explicit error logging in `acquire.py` already provide a loud failure. A monitoring step (e.g., checking that all four series returned data before proceeding) would catch this faster.

### 6. All-NaN Final Row
**Risk:** FRED series have different update cadences. At the end of a reporting period, one or more series may not yet have published the latest month's value. The outer join produces a row with NaN values for those series. `dropna(how="all")` keeps this row if at least one series has data, and the S_score will be computed from incomplete inputs.  
**Likelihood:** Medium — likely to happen on any run near a month boundary.  
**Impact:** The S_score for the current month may be computed from 2–3 series instead of 4, silently reducing its reliability.  
**Mitigation:** Add a `dropna(how="any")` option (configurable) to enforce complete-row-only scoring when strict data integrity is required.

---

## Architectural Risks

### 7. S_score Weighting Formula Not Matching Problem Statement
**Risk:** Foundation 2 defines `S = w1(ΔIP) + w2(ΔCapUtil) - w3(ΔPPI) + w4(ΔInv)` — PPI should carry a **negative** weight because rising prices are a bad supply signal. The current `transform.py` applies equal positive weights to all four series, treating rising prices the same as rising production. This produces a less accurate supply health signal.  
**Likelihood:** Already present in the current implementation.  
**Impact:** The OVERBUY recommendation may trigger too late (price spike masked by production gain) or not at all in a realistic shortage scenario.  
**Mitigation:** Expose a `weights` parameter with asymmetric defaults: `{"IPG3344S": 1.0, "CAPUTLG3344SQ": 1.0, "A34STI": 1.0, "PCU334413334413": -1.0}`. The `weights` parameter already exists in `transform_combined()`; it just needs correct defaults.

### 8. Single Point of Failure: `combined.csv`
**Risk:** `pipeline.py` writes `combined.csv` from `acquire.py`, then re-reads it to pass to `transform.py`. If the file write fails silently (e.g., disk full), `pipeline.py` will attempt to read a stale or empty file and produce wrong output.  
**Likelihood:** Very low.  
**Impact:** Silent bad output — the pipeline would not crash, it would just transform stale data.  
**Mitigation:** The `pd.read_csv` call in `pipeline.py` should verify that the file modification time is within the current run's timeframe, or `fetch_all` should return the DataFrame directly (avoiding the round-trip through disk entirely).

### 9. No Validation Filter at Transformation Boundary
**Risk:** Foundation 2 architecture specifies a dedicated "Validation Filter" that asserts all inputs are in percentage form before the S_score calculation runs. This filter does not currently exist. If `pct_change()` fails silently (e.g., returns raw values due to an upstream bug), the pipeline will compute an S_score from non-normalized units.  
**Likelihood:** Low in normal operation; higher during development when series are swapped.  
**Impact:** Mathematically fraudulent S_score — the exact Data Integrity failure the architecture was designed to prevent.  
**Mitigation:** Add a pre-calculation assertion in `transform.py` that all values in the rolling DataFrame are within a reasonable percentage range (e.g., between -1.0 and 1.0 for monthly data), raising a `ValueError` if not.
