---
title: Code Conventions
mapped: 2026-05-04
---

# Code Conventions

## Code Style

- **Formatter:** Ruff (`ruff-format`) — double quotes, 4-space indent, 88-char line length
- **Linter:** Ruff with rules: E, W, F, I, B, C4, UP, ARG, SIM, TCH, PTH, PL, RUF
- **Enforced on:** `Foundation*` directories via pre-commit hooks
- **Katas:** Not enforced by pre-commit; style varies by exercise

## Naming Conventions

- **Files:** `snake_case.py` (e.g., `acquire.py`, `transform.py`, `run_pipeline.py`)
- **Functions:** `snake_case` (e.g., `get_fred_series_with_payload`, `compute_rolling_mean`)
- **Classes:** `PascalCase` (e.g., `WeatherStats`, `ShortageScoutPipeline`)
- **Constants:** `UPPER_SNAKE_CASE` (e.g., `FRED_API_KEY`, `DEFAULT_SERIES`)
- **Test files:** `test_*.py` prefix

## Import Style

- isort enforced via Ruff (`I` rules)
- `known-first-party = ["cidm6330"]` in pyproject.toml
- Standard lib → third-party → first-party order

## Error Handling Philosophy

- **"Fail loudly"** — pipeline crashes rather than silently passing bad data
  - Risk markers in Foundation3 (`# Risk 4`, `# Risk 9`) annotate validation decisions
- Validation filter in `Foundation3/transform.py`: percent-change values outside [-1.0, 1.0] flagged
- Series completeness check in `Foundation3/pipeline.py`: asserts all requested series were fetched
- `# Risk 8` — explicit guard against silent stale-file reads (data read from memory, not re-read from disk)

## Logging & Observability

- Python `logging` module for pipeline observability
- `structlog` installed (used in gzkit context, not core pipeline)
- Comprehensive logging at key pipeline stages for auditability

## Documentation / Comments

- Inline `# Risk N` comments annotate design decisions in Foundation3
- AAA (Arrange-Act-Assert) pattern documented in test comments
- README files in each subdirectory explain the exercise/module

## Data Handling

- **Auditability first:** Raw JSON archived with vintage date before transformation
- **Deterministic outputs:** Synthetic data generators use fixed seeds for reproducibility
- **Asymmetric weights:** PPI contribution to S-score is negative (documented in `# Risk 7`)

## Type Checking

- **ty** (Astral) configured for Python 3.13
- Not yet integrated into pre-commit (manual: `uv run ty check .`)

## Dependency Management Pattern

- Production deps pinned in `requirements.txt`
- Dev deps loosely pinned in `requirements-dev.txt`
- `pyproject.toml` for project metadata and tool config
- `uv.lock` for pre-commit reproducibility
