---
title: Technology Stack
mapped: 2026-05-04
---

# Technology Stack

## Language & Runtime

- **Python 3.13+** — primary language (`requires-python = ">=3.13"` in `pyproject.toml`)
- **Node.js v24** — present for GSD tooling only; not used in application code

## Frameworks & Libraries

### Data & Pipeline
| Package | Version | Purpose |
|---------|---------|---------|
| `pandas` | >=2.0,<3.0 | DataFrames for FRED series transformation |
| `requests` | 2.32.3 | HTTP client for FRED API calls |
| `python-dotenv` | latest | `.env` file loading for `FRED_API_KEY` |
| `SQLAlchemy` | 2.0.38 | ORM used in Kata2 SQLite exercises |

### Web Frameworks (course exercises only)
| Package | Version | Purpose |
|---------|---------|---------|
| `Django` | 5.1.6 | Course exercise — REST API |
| `djangorestframework` | 3.15.2 | DRF for Django REST APIs |
| `fastapi` | 0.115.8 | Course exercise — async API |
| `Flask` | 3.1.0 | Course exercise — lightweight API |
| `uvicorn` | 0.34.0 | ASGI server for FastAPI |

### Async / Task Queue (course exercises)
| Package | Version | Purpose |
|---------|---------|---------|
| `celery` | 5.4.0 | Distributed task queue exercises |
| `channels` | 4.2.0 | Django async/WebSocket exercises |
| `channels_redis` | 4.2.1 | Redis channel layer |
| `redis` | 5.2.1 | Redis client |

### Validation
| Package | Version | Purpose |
|---------|---------|---------|
| `pydantic` | 2.10.6 | Data validation (dev/exercises) |

## Tooling

### Linting & Formatting
- **Ruff** — replaces black, isort, flake8, pylint (`pyproject.toml` rules: E, W, F, I, B, C4, UP, ARG, SIM, TCH, PTH, PL, RUF)
- Applied to Foundation directory via pre-commit (`files: ^Foundation`)
- Line length: 88, quote-style: double, indent: spaces

### Type Checking
- **ty** (Astral) — configured in `pyproject.toml` under `[tool.ty]`
- Target: Python 3.13

### Pre-commit
- `check-added-large-files` (max 1024KB)
- `check-toml`, `check-yaml`
- `end-of-file-fixer`, `trailing-whitespace`
- `ruff` + `ruff-format` on Foundation files

### Testing
- **pytest** — primary test runner
- `responses` library — HTTP mocking
- `unittest.mock` — patching

### Package Management
- **pip** + `.venv` — project virtual environment at `.venv/`
- `requirements.txt` — pinned production deps
- `requirements-dev.txt` — dev/test deps
- `uv.lock` present (uv used by pre-commit, not primary workflow)

## Configuration Files

| File | Purpose |
|------|---------|
| `pyproject.toml` | Project metadata, ruff, ty config |
| `requirements.txt` | Pinned full dependency list |
| `requirements-dev.txt` | Dev dependencies |
| `.pre-commit-config.yaml` | Pre-commit hooks |
| `.env` | `FRED_API_KEY` secret (gitignored) |
| `.editorconfig` | Editor settings |
| `.vscode/` | VS Code workspace settings |
| `uv.lock` | uv lock file (pre-commit usage) |

## CI/CD

- **GitHub Actions** — `.github/workflows/ci.yml`
- Runs on push/PR

## Key Entry Points

- `run_pipeline.py` — CLI entry point for Shortage Scout pipeline (argparse, `--demo`, `--start-date`, `--end-date`)
- `Foundation3/pipeline.py` — Core pipeline orchestration
- `Foundation3/acquire.py` — FRED API data acquisition
- `Foundation3/transform.py` — Data transformation (MoM%, rolling mean, S-score)
