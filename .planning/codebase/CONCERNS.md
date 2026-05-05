---
title: Technical Concerns
mapped: 2026-05-04
---

# Technical Concerns

## Known Bugs

### Empty CSV Crash (Kata9)
- **File:** `Katas/Kata9/test_integration.py:231-235`
- **Issue:** Empty CSV input causes `TypeError`/`AttributeError` in pipeline
- **Status:** Documented as known; pipeline hardening deferred
- **Risk:** Medium — only occurs on empty input edge case

### Kata9 Pipeline is a Direct Copy
- **File:** `Katas/Kata9/pipeline.py:2`
- **Comment:** `# NOTE: This file is a direct copy of Katas/Kata4/pipeline.py`
- **Risk:** Low — exercise code, but indicates Kata9 is not independently maintained

## Technical Debt

### Dependency Sprawl
- `requirements.txt` contains 98 pinned packages covering Django, FastAPI, Flask, Celery, Channels, Redis, Twisted — most are course exercise dependencies not used in the production pipeline
- No separation between pipeline runtime deps and course exercise deps
- Risk: Bloated install, version conflicts hard to trace

### Dual Package Manager Confusion
- `uv.lock` exists (from pre-commit's uv usage) but `pip` is the primary workflow
- `requirements-dev.txt` pins `pydantic==2.10.6` but gzkit install upgraded pydantic to 2.13.3 (now removed, but venv state may have drift)
- `black==25.1.0` in `requirements-dev.txt` is legacy — ruff-format is preferred

### Linting Applied Inconsistently
- Ruff pre-commit hook only applies to `Foundation*` directories (`files: ^Foundation`)
- `Katas/`, `Testing/`, `tutorials/` are not linted in CI
- Risk: Code quality varies across the repo

### No Enforced Test Coverage
- `.coverage` file exists but no coverage threshold in CI or pyproject.toml
- `Katas/Kata9/test_integration.py` has documented untested edge cases

### Type Checking Not in CI
- `ty` is configured but not integrated into `.pre-commit-config.yaml` or `ci.yml`
- Manual invocation only

## Architecture Concerns

### Hardcoded Series List
- **File:** `run_pipeline.py`
- Default FRED series `["IPG3344S", "CAPUTLG3344SQ", "A34STI", "PCU334413334413"]` hardcoded in script
- Should be configurable via config file for extensibility

### No Pipeline Orchestration Framework
- `Foundation3/pipeline.py` is a flat sequential script; no DAG, retry-per-step, or partial failure recovery
- Acquire failure aborts the entire pipeline with no checkpoint/resume

### Demo Mode Logic in Entry Point
- `run_pipeline.py` mixes mode-detection logic (API key present?) with pipeline invocation
- Coupling makes testing the entry point harder

## Security

### API Key in .env
- `FRED_API_KEY` stored in `.env` — gitignored, but no secrets manager
- No validation that `.env` exists before pipeline runs (fails with unhelpful KeyError if missing)

### No Input Sanitization
- FRED series IDs passed directly to API; no validation of format before request

## Performance

### No Caching of FRED Responses
- Each pipeline run makes fresh API calls; repeated runs for same date range re-fetch
- Vintage date archival writes raw JSON but doesn't serve as a cache

### Sequential Series Fetching
- `Foundation3/acquire.py` fetches each FRED series sequentially
- Could be parallelized with `concurrent.futures` for faster acquisition

## Fragile Areas

### Risk-Annotated Code in Foundation3
- `# Risk 4` — vintage date archival (auditability)
- `# Risk 5` — series completeness verification (crashes if series missing)
- `# Risk 7` — asymmetric weights (PPI is negative; easy to break)
- `# Risk 8` — stale-file guard (data read from memory, not re-read from disk)
- `# Risk 9` — percent-change filter [-1.0, 1.0] (may reject valid extreme values)

### S-Score Weight Sensitivity
- Weighted S-score in `Foundation3/transform.py` uses hand-tuned weights
- Asymmetric contribution (PPI negative) makes the formula easy to break silently
- No automated test validates that weight changes are intentional

## Course Project Structure Note
This repo is a **course project** (CIDM 6330 — Software Systems Development). Many directories (`Katas/`, `Testing/`, `tutorials/`, course framework exercises) are pedagogical and not part of the production Shortage Scout pipeline. The "real" application code lives in `Foundation3/` and is driven by `run_pipeline.py`.
