---
title: Architecture
mapped: 2026-05-04
---

# Architecture

## Pattern

**Pipes and Filters (Pipeline Architecture)**

Chosen for its alignment with monthly batch processing: simple sequential data flow, strong auditability, easy local testing, and reproducible outputs. Microservices and serverless were explicitly evaluated and rejected (see `Foundation1/ARCH_CHAR.md`).

## System Overview

This repo contains two tracks:

1. **Shortage Scout** — the capstone production pipeline (`Foundation3/` + `run_pipeline.py`)
2. **Course Katas** — skill-building exercises (Kata1–Kata10) demonstrating progressively advanced patterns

---

## Shortage Scout Pipeline (Foundation3)

### Three-Stage Architecture

```
[FRED API] → acquire.py → [raw JSON archive] → transform.py → [S_score] → [JSON/CSV output]
```

### Stage 1: Acquire (`Foundation3/acquire.py`)
- Fetches each FRED series via HTTP with exponential backoff retry (2 retries, 1.5x backoff)
- Dual persistence per series:
  - `{series_id}.csv` — human-readable
  - `{series_id}_{timestamp}.json` — raw FRED payload with vintage date (auditability, Risk 4)
- Combines all series into `combined.csv`
- Returns `dict[str, pd.Series]` in memory — downstream never re-reads disk (Risk 8)

### Stage 2: Transform (`Foundation3/transform.py`)
Five sequential operations on the combined DataFrame:
1. **Percent change** — `pct_change()` month-over-month
2. **Null handling** — `dropna(how='any')` in strict mode (Risk 6)
3. **Range validation** — asserts all values ∈ [-1.0, 1.0] (Risk 9)
4. **Rolling mean** — 3-month window
5. **Weighted S-score** — asymmetric weights (PPI weight is negative, Risk 7)

```python
ASYMMETRIC_WEIGHTS = {
    "IPG3344S": 1.0,           # Industrial production (supply)
    "CAPUTLG3344SQ": 1.0,      # Capacity utilization (supply)
    "A34STI": 1.0,             # Shipments/inventories (supply)
    "PCU334413334413": -1.0,   # PPI semiconductor (demand pressure, inverted)
}
```

### Stage 3: Orchestration (`Foundation3/pipeline.py`)
- Validates all requested series were fetched before proceeding (Risk 5)
- Builds combined DataFrame from in-memory dict (not from disk)
- Emits `results/transformed.json`

### Entry Point (`run_pipeline.py`)
- CLI via argparse: `--start-date`, `--end-date`, `--demo`
- Demo mode (no API key or `--demo` flag): uses `Foundation3/generate_sample.py`
- Real mode: delegates to `Foundation3/pipeline.py`

### Recommendation Output
```
S_score < 0  →  OVERBUY  (declining supply signals = contraction)
S_score ≥ 0  →  HOLD
```

---

## Katas — Design Patterns by Layer

| Kata | Pattern | Key Concept |
|------|---------|------------|
| Kata1 | Filter + Transform | WeatherFilter, format auto-detection |
| Kata2 | Repository (manual) | Dataclasses + explicit SQL, no ORM |
| Kata3 | Resilience | Exponential backoff retry (max 6 attempts) |
| Kata4 | Pipes & Filters | `extract → transform → load → report` (generator-based) |
| Kata5 | Concurrency | `ThreadPoolExecutor`, `threading.Lock` for thread-safe writes |
| Kata6 | Algorithm | Binary search via `bisect` module |
| Kata7 | Observability | JUnit XML, HTML coverage reporting |
| Kata8 | Test doubles | `unittest.mock`, `responses` library |
| Kata9 | Integration | End-to-end with synthetic 1000-row FRED data |
| Kata10 | TDD | Red-Green-Refactor cycle, depends on Kata1 |

---

## Data Flow

```
FRED API (external)
     │
     ▼
acquire.py ──────────────────────────────────────────────────────────────┐
     │  retries, backoff                                                   │
     ├─→ {series_id}.csv (human-readable)                                 │
     ├─→ {series_id}_{ts}.json (raw audit archive)                        │
     └─→ dict[str, pd.Series] (in-memory) ──→ combined.csv              │
                                     │                                     │
                                     ▼                                     │
                              transform.py                                │
                                     │                                     │
                                     ├─ pct_change                        │
                                     ├─ dropna                            │
                                     ├─ validate [-1, 1]                  │
                                     ├─ rolling(3)                        │
                                     └─ weighted S_score                  │
                                               │                           │
                                               ▼                           │
                                    results/transformed.json ◄─────────────┘
                                    OVERBUY / HOLD recommendation
```

---

## Key Architectural Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Batch vs. streaming | Batch | Monthly FRED data cadence; streaming adds complexity with no benefit |
| Single-process vs. distributed | Single-process | Auditability, local testing, batch size manageable |
| Fail loudly vs. silently | Fail loudly | ValueError on invalid data; pipeline aborts rather than producing bad output |
| Real vs. synthetic data in tests | Synthetic | Hermetic, reproducible, no network I/O in tests |
| Read from memory vs. disk | Memory | Eliminates stale-file scenario (Risk 8) |
| Weights symmetric vs. asymmetric | Asymmetric | PPI is demand-side pressure, negatively correlated with shortage |

---

## CI Gates

Only two test suites are CI-gated (`.github/workflows/ci.yml`):
1. `Foundation3/tests` — critical pipeline tests (quiet mode)
2. `Katas/Kata9/test_integration.py` — end-to-end integration (verbose)

All other Kata tests run locally only.
