# MVP Test Coverage

**Project:** Shortage Scout — FRED economic time-series pipeline

---

## How to run the tests

```bash
# all project tests (no API key required)
pytest Foundation3/tests/ -v

# with coverage report
pytest Foundation3/tests/ --cov=Foundation3 --cov-report=term-missing
```

All tests run against a deterministic fake — no network access or `FRED_API_KEY` needed.

---

## 1. Unit Tests

Unit tests isolate individual functions with controlled inputs and assert on specific outputs. No I/O, no network, no side effects.

### test_transform.py — `Foundation3/tests/test_transform.py`

Tests the core business logic in `transform_combined`.

| Test | What it asserts | Why it matters |
|---|---|---|
| `test_transform_declining_supply_triggers_overbuy` | A series declining ~3 % per month produces a **negative** `S_score` and `Recommendation == "OVERBUY"` | Core business rule: contraction in supply health must trigger a buy signal |
| `test_transform_computes_s_score_and_recommendation` | A series growing exactly 10 % per month produces rolling metrics of `0.10` and `Recommendation == "HOLD"` | Validates the arithmetic of `pct_change` + 3-month rolling mean + equal-weight mean |

**Notable assertions:**

```python
# Declining supply → negative score → OVERBUY
assert last["S_score"] < 0
assert last["Recommendation"] == "OVERBUY"

# Stable growth → exact numeric rolling mean → HOLD
assert round(last["S_score"], 6) == round(0.1, 6)
assert last["Recommendation"] == "HOLD"
```

### test_transform_weights.py — `Foundation3/tests/test_transform_weights.py`

Tests the asymmetric weighting logic in isolation.

| Test | What it asserts | Why it matters |
|---|---|---|
| `test_weighted_s_score` | With `weights={"A": 1.0, "B": 0.0}`, the `S_score` equals series A's rolling metric exactly | Confirms PPI's `-1.0` weight (and any zero-weight series) are applied correctly before the S_score is calculated |

```python
weights = {"A": 1.0, "B": 0.0}
out = transform_combined(df, weights=weights, threshold=0.0)
assert round(last["S_score"], 6) == round(last["A"], 6)
```

This test directly covers the production configuration where `PCU334413334413` carries `-1.0` so rising prices subtract from rather than inflate the supply score.

---

## 2. Integration Tests

Integration tests verify that multiple components work together end-to-end, using the same fake-HTTP boundary as unit tests but exercising the full data-flow path.

### test_acquire.py — `Foundation3/tests/test_acquire.py`

Tests `fetch_all` (acquisition module) with a monkeypatched HTTP layer.

| Test | What it asserts | Why it matters |
|---|---|---|
| `test_fetch_all_writes_files` | Given a fake `get_fred_series_with_payload`, `fetch_all` writes per-series `.csv` files, a `combined.csv`, and returns a dict keyed by series ID | Verifies the acquisition → file-write → return-value chain without touching the network |

```python
def fake_get_fred_series_with_payload(_series_id, **_kwargs):
    dates = pd.to_datetime(["2020-01-31", "2020-02-29", "2020-03-31"])
    df = pd.DataFrame({"value": [1.0, 2.0, 3.0]}, index=dates)
    return df, {"observations": []}

monkeypatch.setattr(acq, "get_fred_series_with_payload", fake_get_fred_series_with_payload)
frames = fetch_all(["S1", "S2"], tmp_path / "results")

assert set(frames.keys()) == {"S1", "S2"}
assert (out / "S1.csv").exists()
assert (out / "combined.csv").exists()
```

The integration boundary here is `fetch_all` → disk. The test confirms:
- Both per-series CSVs are written.
- `combined.csv` is produced with the correct columns.
- The return dict can be handed directly to `transform_combined` (the next pipeline stage).

---

## 3. Test Suite Summary

### Coverage map

| Concern | Covered | How |
|---|---|---|
| Percent-change computation | Yes | `test_transform_computes_s_score_and_recommendation` — exact numeric assertion |
| 3-month rolling mean | Yes | Same test — verifies rolling mean stabilises to true pct-change after 3 periods |
| S_score weighted average | Yes | `test_weighted_s_score` — zero-weight series excluded from result |
| Asymmetric (negative) weights | Yes | `test_weighted_s_score` — implicitly; the B series (weight 0) cannot raise S_score |
| OVERBUY recommendation trigger | Yes | `test_transform_declining_supply_triggers_overbuy` |
| HOLD recommendation trigger | Yes | `test_transform_computes_s_score_and_recommendation` |
| `fetch_all` file output | Yes | `test_fetch_all_writes_files` |
| `fetch_all` return value shape | Yes | `test_fetch_all_writes_files` — asserts on dict keys |
| FRED HTTP layer (real) | No — intentional | Tests mock the HTTP call; real-API smoke testing is done manually (see §4) |
| Retry / back-off logic | No | Not yet tested; retry is exercised implicitly by the fake raising exceptions in future work |
| `transform_combined` with `strict=True` | No | Drop-any-NaN path not yet covered by a test |
| Range-validation guard (`[-1.0, 1.0]`) | No | `ValueError` raise path not yet covered by a test |
| `run_pipeline.py` end-to-end CLI | No | Covered by the demo run (`python run_pipeline.py --demo`) but not automated |

### What is not covered and why

**Real HTTP / FRED API** — unit and integration tests replace the HTTP layer with a deterministic fake. This is intentional: tests that hit the live API are fragile (rate limits, network, API key rotation), non-deterministic, and unsuitable for CI. The trade-off is that changes to `FRED_helper.py`'s parsing logic are not caught until a real run.

**Retry and back-off** — the retry loop in `acquire.fetch_all` requires the fake to raise exceptions on the first N attempts. These tests are straightforward to add and are flagged as a known gap.

**`strict=True` NaN-drop path** — the `strict` parameter selects `how="any"` instead of `how="all"`. No test currently exercises this path, so a regression would not be caught.

**Range-validation `ValueError`** — the guard that raises when a `pct_change` value exceeds `[-1.0, 1.0]` is untested. A test passing raw-normalised data (e.g., values in the hundreds) should be added.

---

## 4. Quality Evidence

### CI — GitHub Actions

**File:** [.github/workflows/ci.yml](../.github/workflows/ci.yml)

```yaml
on:
  push:
    branches: [ main, master ]
  pull_request:
    branches: [ main, master ]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
        with:
          python-version: "3.11"
      - run: pip install -r requirements.txt -r requirements-dev.txt
      - run: python -m pytest -q Foundation3/tests
```

Tests run automatically on every push and pull request to `main`/`master`. No `FRED_API_KEY` secret is required because all tests mock the HTTP layer.

### Local test run (green)

```
============================= test session starts =============================
platform win32 — Python 3.13.3, pytest-9.0.2
collected 4 items

Foundation3/tests/test_acquire.py::test_fetch_all_writes_files        PASSED
Foundation3/tests/test_transform.py::test_transform_declining_supply_triggers_overbuy  PASSED
Foundation3/tests/test_transform.py::test_transform_computes_s_score_and_recommendation PASSED
Foundation3/tests/test_transform_weights.py::test_weighted_s_score    PASSED

============================== 4 passed in 0.62s ==============================
```

### Test fix note

During Foundation 4 test review, `test_acquire.py` was found to be patching `get_fred_series` — a name that no longer exists in `acquire.py`'s namespace after the module was upgraded to use `get_fred_series_with_payload`. The monkeypatch target and the fake's return type were corrected to match the current interface (`(df, payload)` tuple). The fix is in [Foundation3/tests/test_acquire.py](../Foundation3/tests/test_acquire.py).
