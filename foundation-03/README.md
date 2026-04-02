# Foundation 3/4 - GDP FRED Pipeline MVP

This folder contains the runnable GDP/FRED pipeline that serves as the delivered MVP for Foundation 4. The system is a modular monolith organized as a pipeline: acquire data, transform it into analytical indicators, and produce inspectable output artifacts.

## Problem Alignment

The project addresses the Foundation 2 problem statement of monitoring U.S. economic growth with reproducible GDP trend analysis. The pipeline focuses on FRED Real GDP (`GDPC1`) and produces derived indicators that help identify potential downturn signals.

## What the MVP Does

- Acquires GDP observations from a built-in sample payload by default
- Optionally calls the live FRED observations endpoint when `USE_LIVE_FRED=true` and a valid `FRED_API_KEY` is available
- Cleans invalid rows, enforces chronological ordering, and removes duplicate dates
- Computes:
  - `gdp_level`
  - `qoq_pct_change`
  - `yoy_pct_change`
  - `rolling_4q_change`
  - `signal_flag`
  - `signal_reasons`
- Writes raw JSON, transformed JSON, and a markdown run summary

## Run the MVP

From `foundation-03`:

```powershell
python -m pipeline.run_pipeline
```

## Optional Live FRED Mode

Set these environment variables before running:

- `USE_LIVE_FRED`
- `FRED_API_KEY`
- `FRED_SERIES_ID`
- `FRED_OBSERVATION_START`
- `FRED_OBSERVATION_END`
- `FRED_REQUEST_TIMEOUT_SECONDS`
- `FRED_MAX_RETRIES`
- `FRED_RETRY_BACKOFF_SECONDS`
- `FRED_FALLBACK_TO_SAMPLE_ON_ERROR`

Example:

```powershell
$env:USE_LIVE_FRED="true"
$env:FRED_API_KEY="your_key_here"
$env:FRED_SERIES_ID="GDPC1"
python -m pipeline.run_pipeline
```

## Test the MVP

```powershell
python -m unittest discover -s pipeline/tests -p "test_*.py"
```

The suite includes both unit and integration tests. Detailed coverage notes are documented in [foundation-04/TESTING.md](../foundation-04/TESTING.md).

## Key Outputs

- `data/raw/gdp_raw.json`
- `data/transformed/gdp_transformed.json`
- `output/reports/pipeline_run_summary.md`

## Deployment / Execution Notes

- The MVP runs locally with the Python standard library and does not require third-party packages.
- Sample mode is the default so the system remains runnable even without internet access.
- Live mode depends on external connectivity and a valid FRED API key.

## Demonstration Support

Foundation 4 documentation for demonstration and defense lives in [foundation-04](../foundation-04/README.md), including:

- demo script
- testing documentation
- ADRs
- architecture diagram
- reflection
- PR summary draft

## Current Limitations

- No CI workflow is configured yet
- Live API behavior is not covered by end-to-end automated tests
- Storage remains file-based rather than database-backed
- Observability is lightweight and focused on course-MVP needs
