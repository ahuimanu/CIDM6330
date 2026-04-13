# MVP Iteration 1 — Data Acquisition

**Project:** Shortage Scout — FRED economic time-series pipeline  
**Goal:** Compute an `S_score` from FRED series to support semiconductor inventory recommendations.

---

## 1. Working Code

### Entry point — CLI pipeline runner

**File:** [run_pipeline.py](../run_pipeline.py)

```
python run_pipeline.py                                    # auto-detects key, or falls back to demo
python run_pipeline.py --demo                             # force synthetic data (no key required)
python run_pipeline.py --start-date 2020-01-01 --end-date 2023-12-31
```

The runner auto-detects `FRED_API_KEY` from the environment (or a `.env` file in the repo root). If the key is absent or `--demo` is passed, it runs a fully synthetic pipeline so the code is **always runnable without credentials**.

### Acquisition module

**File:** [Foundation3/acquire.py](../Foundation3/acquire.py)

`fetch_all(series_list, out_dir, start_date, end_date, retries, backoff)` is the primary acquisition function. It:

- Calls `get_fred_series_with_payload` for each series.
- Writes a per-series `.csv` and a timestamped raw `.json` payload to `out_dir`.
- Concatenates all series into `combined.csv`.
- Returns a `dict[str, pd.Series]` used directly by the downstream pipeline (no disk re-read).

### FRED HTTP client

**File:** [Foundation1/FRED_helper.py](../Foundation1/FRED_helper.py)

Two functions:

| Function | Returns |
|---|---|
| `get_fred_series(series_id, ...)` | `pd.DataFrame` with `date` index and `value` column |
| `get_fred_series_with_payload(series_id, ...)` | `(pd.DataFrame, dict)` — DataFrame + full raw JSON payload (vintage metadata) |

The raw payload includes FRED's per-observation `realtime_start`/`realtime_end` fields, preserving point-in-time auditability.

### Demo / synthetic fallback

**File:** [Foundation3/generate_sample.py](../Foundation3/generate_sample.py)

Generates a 5-month synthetic dataset modelling a contraction scenario (production and inventory falling, prices rising) and runs the full transform. Used by `--demo` mode and in CI.

---

## 2. Data Samples

### combined.csv (sample — synthetic demo run)

```
,IPG3344S,CAPUTLG3344SQ,A34STI,PCU334413334413
2021-01-31,100.0,70.0,50.0,200.0
2021-02-28,105.0,71.4,52.5,198.0
2021-03-31,110.25,72.828,55.125,197.01
2021-04-30,115.7625,74.28456,57.88125,196.0399
2021-05-31,121.5506,75.7732512,60.7753125,195.079501
```

**Series:**

| FRED ID | Meaning | Direction |
|---|---|---|
| `IPG3344S` | Industrial Production — Semiconductor mfg | positive supply signal |
| `CAPUTLG3344SQ` | Capacity Utilization — Semiconductor mfg | positive supply signal |
| `A34STI` | Manufacturers' Inventories — Computers & Electronics | positive supply signal |
| `PCU334413334413` | PPI — Semiconductor mfg | negative supply signal (rising prices = supply pressure) |

### transformed.json (sample output)

```json
[
  {
    "index": "2021-04-30T00:00:00.000",
    "IPG3344S": 0.05,
    "CAPUTLG3344SQ": 0.02,
    "A34STI": 0.05,
    "PCU334413334413": -0.006641,
    "S_score": 0.028339,
    "Recommendation": "OVERBUY"
  },
  {
    "index": "2021-05-31T00:00:00.000",
    "IPG3344S": 0.049999,
    "CAPUTLG3344SQ": 0.020013,
    "A34STI": 0.05,
    "PCU334413334413": -0.004941,
    "S_score": 0.028768,
    "Recommendation": "OVERBUY"
  }
]
```

The `S_score` is a weighted mean of month-over-month pct-changes. `PCU` carries a weight of `-1.0` so rising prices subtract from the score. The `Recommendation` field is `OVERBUY` when `S_score > 0` (supply is expanding / price pressure is low) and `UNDERBUY` when `S_score <= 0`.

All artifacts are written to `Foundation3/results/`.

---

## 3. Error Handling

### API key missing

```python
# Foundation1/FRED_helper.py — get_api_key()
def get_api_key() -> str:
    key = os.getenv("FRED_API_KEY")
    if key:
        key = key.strip()
    if not key:
        raise RuntimeError("FRED_API_KEY not set in env or .env")
    return key
```

`run_pipeline.py` catches the absent-key case before attempting any HTTP call and falls back to the demo pipeline automatically, printing a clear message:

```
FRED_API_KEY not found — running demo pipeline using synthetic data.
```

### Network failures and rate limiting — retry with exponential back-off

```python
# Foundation3/acquire.py — fetch_all()
while attempt <= retries:
    try:
        df, payload = get_fred_series_with_payload(s, ...)
        ...
        break
    except Exception as e:
        last_exc = e
        attempt += 1
        logger.warning("Attempt %d failed for %s: %s", attempt, s, e)
        logger.debug("Exception details", exc_info=e)
        time.sleep(backoff * attempt)   # 1.5s, 3.0s, 4.5s …
else:
    logger.error("Failed to fetch %s after %d attempts: %s", s, retries + 1, last_exc)
```

Default: 2 retries, 1.5 s back-off multiplier. All failures are logged at `ERROR` level with the full exception chain available at `DEBUG`.

### HTTP errors

`requests.Session.get(...).raise_for_status()` in `FRED_helper.py` converts any 4xx/5xx response (including `429 Too Many Requests`) into a `requests.HTTPError`, which bubbles up to the retry loop above.

### Empty / malformed observations

```python
# Foundation1/FRED_helper.py
df["value"] = pd.to_numeric(df["value"].replace(".", pd.NA))
```

FRED encodes missing observations as the string `"."`. This line converts them to `pd.NA` rather than silently producing `NaN`-poisoned arithmetic. If the entire response is empty, `fetch_all` logs a warning and skips that series:

```python
if df.empty:
    logger.warning("No data returned for %s", s)
    break
```

### Partial fetch (some series missing)

```python
# Foundation3/pipeline.py — run_pipeline()
missing = [s for s in series_list if s not in frames]
if missing:
    logger.warning("Missing series (discontinued or fetch failed): %s", missing)
```

The pipeline continues with whatever series were successfully fetched and warns about gaps — it does not silently drop data or abort on a single series failure.

### Empty combined result

```python
if not frames:
    logger.error("No series fetched; nothing to save")
    return {}
```

If acquisition yields nothing at all, `fetch_all` returns an empty dict and `run_pipeline` logs an error and exits cleanly.

---

## 4. Documentation

### How to run

**Prerequisites:**

```bash
pip install -r requirements.txt
```

**With a FRED API key** (free registration at [fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html)):

```bash
# Create .env in repo root
echo "FRED_API_KEY=your_key_here" > .env

# Run pipeline (default: full history)
python run_pipeline.py

# Run with date range
python run_pipeline.py --start-date 2020-01-01 --end-date 2023-12-31
```

**Without a key (demo mode — always works):**

```bash
python run_pipeline.py --demo
```

Outputs are written to `Foundation3/results/`:

| File | Contents |
|---|---|
| `{SERIES_ID}.csv` | Raw per-series observations |
| `{SERIES_ID}_{timestamp}.json` | Raw FRED JSON payload with vintage metadata |
| `combined.csv` | All series joined on date index |
| `transformed.json` | `S_score` and `Recommendation` per period |
| `pipeline.log` | Log file (demo mode) |

### Running tests (no API key required)

```bash
pytest Foundation3/tests/
```

Tests use `monkeypatch` to replace the HTTP layer with a deterministic fake, so they run in CI without any credentials.

### Inline documentation

- [Foundation1/FRED_helper.py](../Foundation1/FRED_helper.py) — docstring on `get_fred_series_with_payload` explains the vintage-metadata return value and its role in point-in-time auditability.
- [Foundation3/acquire.py](../Foundation3/acquire.py) — function signature with full parameter documentation; logging statements serve as inline execution trace.
- [Foundation3/pipeline.py](../Foundation3/pipeline.py) — inline comments reference the specific architectural risks (Risk 4, 5, 7, 8) each guard addresses, traceable to [Foundation3/RISK_IDENTIFICATION.md](../Foundation3/RISK_IDENTIFICATION.md).
- [Foundation3/README.md](../Foundation3/README.md) — quick-start guide covering environment setup, CLI usage, test execution, and CI behaviour.
