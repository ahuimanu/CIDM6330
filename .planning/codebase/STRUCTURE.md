---
title: Directory Structure
mapped: 2026-05-04
---

# Directory Structure

## Top-Level Layout

```
CIDM6330-Spring2026-Patrick-Perez/
├── Foundation1/          # Lead-lag analysis (FRED helper + correlation)
├── Foundation2/          # Architecture exploration artifacts
├── Foundation3/          # Shortage Scout pipeline (main application)
├── Foundation4/          # Foundation 4 exercises
├── Foundations/          # Roman numerals kata (educational)
├── Katas/                # Kata1–Kata10 skill exercises
├── CIDM6330/             # Course materials directory (currently empty)
├── Testing/              # Additional testing exercises (Hillard, PyTesting)
├── tutorials/            # Roman numerals and other tutorials
├── Shortage_research/    # Research outputs (notebook_outputs/)
├── Merged_repo/          # Merge artifacts
├── scripts/              # Utility scripts
├── docs/                 # Course documentation and guides
├── .claude/              # Claude Code + GSD tooling
├── .github/              # CI workflows, instructions
├── .planning/            # GSD planning artifacts (this file lives here)
├── .venv/                # Python virtual environment
├── run_pipeline.py       # CLI entry point for Shortage Scout
├── pyproject.toml        # Project config (ruff, ty, metadata)
├── requirements.txt      # Pinned production deps (98 packages)
├── requirements-dev.txt  # Dev/test deps
├── .env                  # FRED_API_KEY secret (gitignored)
├── ARCHITECTURE.md       # High-level architecture doc
├── ADR_Guidelines.md     # ADR process guide
├── ADR_Template.md       # ADR template
├── AI_LOG.md             # AI collaboration log
└── Agents.MD             # AI agent guidelines (teaching assistant rules)
```

## Foundation3 (Shortage Scout — Primary Application)

```
Foundation3/
├── pipeline.py           # Orchestrator — fetch → combine → transform → output
├── acquire.py            # FRED API fetcher with retry and dual persistence
├── transform.py          # pct_change → dropna → validate → rolling → S_score
├── generate_sample.py    # Synthetic data generator for demo mode
├── results/              # Output: transformed.json, combined.csv
├── tests/
│   ├── test_acquire.py          # Monkeypatched FRED fetch tests
│   ├── test_transform.py        # S_score and recommendation logic tests
│   └── test_transform_weights.py # Weight-specific behavior tests
├── RISK_IDENTIFICATION.md
├── ARCH_REALITY_CHECK.md
└── DISTRIBUTED_CONSIDERATIONS.md
```

## Foundation1 (FRED Lag Analysis)

```
Foundation1/
├── FRED_fetch.py         # Basic FRED API fetching
├── FRED_helper.py        # Data access layer: get_fred_series(), get_fred_series_with_payload()
├── lag_test.py           # Lead-lag correlation analysis (IPG3344S → CPIAUCSL)
├── fred_data/            # CSV downloads from FRED (CPIAUCSL.csv, FEDFUNDS.csv, etc.)
├── ARCH_CHAR.md          # Architecture characteristics decision
├── DATASET.md            # FRED data source specification
├── PROBLEM_SPACE.md      # Economic shortage context
└── FEEDBACK.md           # Evaluation feedback
```

## Katas Structure

```
Katas/
├── conftest.py           # Shared fixture: tmp_sqlite_db
├── Kata1/
│   ├── weather_filter.py          # WeatherFilter class
│   ├── sample_weather_data.csv
│   └── sample_weather_data.json
├── Kata2/
│   ├── sqlite_kata.py             # Airport, Runway, WeatherReport dataclasses + CRUD
│   ├── example_usage.py
│   └── test_sqlite_kata.py
├── Kata3/
│   ├── src/kata3_api_consumer.py  # FRED fetcher with exponential backoff
│   ├── requirements.txt
│   └── tests/
│       ├── test_api_consumer_mocked.py
│       └── test_api_consumer_with_responses.py
├── Kata4/
│   ├── pipeline.py                # extract → transform → load → report
│   ├── fed_rates.db               # SQLite output
│   └── test_pipeline.py
├── Kata5/
│   ├── concurrent_fetch.py        # ThreadPoolExecutor + Lock
│   ├── config.json
│   └── logs/ results/
├── Kata6/
│   ├── kata6.py                   # bisect-based binary search
│   ├── run_kata6.py
│   └── BISect.md
├── Kata7/
│   ├── generate_report.py         # JUnit XML + HTML coverage
│   ├── junit.xml
│   └── coverage_html/
├── Kata8/
│   └── tests/
│       ├── test_api_consumer_mocked.py
│       └── test_api_consumer_with_responses.py
├── Kata9/
│   ├── pipeline.py                # Copy of Kata4/pipeline.py
│   └── test_integration.py       # 1000-row synthetic integration tests
└── Kata10/
    └── test_weather_stats.py      # TDD cycles (Red-Green-Refactor)
```

## GSD Planning Directory

```
.planning/
└── codebase/             # Codebase map (this mapping session)
    ├── STACK.md
    ├── INTEGRATIONS.md
    ├── ARCHITECTURE.md
    ├── STRUCTURE.md
    ├── CONVENTIONS.md
    ├── TESTING.md
    └── CONCERNS.md
```

## Key File Locations Quick Reference

| Purpose | Path |
|---------|------|
| Pipeline entry point | `run_pipeline.py` |
| Data acquisition | `Foundation3/acquire.py` |
| Data transformation | `Foundation3/transform.py` |
| Pipeline orchestration | `Foundation3/pipeline.py` |
| FRED data access layer | `Foundation1/FRED_helper.py` |
| Shared test fixtures | `Katas/conftest.py` |
| CI workflow | `.github/workflows/ci.yml` |
| Project config | `pyproject.toml` |
| API key | `.env` → `FRED_API_KEY` |
| Pipeline output | `Foundation3/results/` |
| GSD commands | `.claude/commands/gsd/` |
| GSD agents | `.claude/agents/` |

## Naming Conventions

- **Python files:** `snake_case.py`
- **Test files:** `test_*.py` prefix
- **Directories:** Mixed (`Foundation3`, `Kata10`, `Shortage_research`)
- **Output files:** `{series_id}.csv`, `{series_id}_{timestamp}.json`, `transformed.json`
- **Course docs:** `UPPER_CASE.md` (`ARCHITECTURE.md`, `RISK_IDENTIFICATION.md`)
