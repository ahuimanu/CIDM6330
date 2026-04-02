# Testing Documentation

## Test Strategy

The Foundation 4 MVP uses automated unit and integration tests in `foundation-03/pipeline/tests`.

## Coverage Summary

Unit coverage includes:

- Acquisition sample-path behavior
- Acquisition retry/fallback behavior when live calls fail
- Transformation filtering for invalid rows
- Transformation ordering, deduplication, and derived metric calculations
- Signal classification behavior
- Report summary generation

Integration coverage includes:

- End-to-end pipeline execution through `run_pipeline()`
- Artifact creation for raw, transformed, and report outputs
- Report content checks for derived metrics and flagged periods

## Run the Tests

From `foundation-03`:

```powershell
python -m unittest discover -s pipeline/tests -p "test_*.py"
```

## What the Tests Do Not Cover

- Real network calls to the live FRED API
- API key management in a real deployment environment
- Performance under large-volume series retrieval
- Multi-series orchestration, because the MVP remains single-series by design

These gaps are intentional for this course-stage MVP. The automated suite prioritizes determinism, offline repeatability, and verification of the architectural core.

## Quality Evidence

- Automated tests exist and pass locally.
- Manual verification supplements the tests by running the pipeline and inspecting generated artifacts.
- CI/CD automation is not currently configured. Manual verification steps are documented in [DEMO_SCRIPT.md](DEMO_SCRIPT.md).
