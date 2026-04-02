# Foundation 4 Demo Script

## Goal

Demonstrate that the GDP/FRED pipeline runs end to end, produces analysis-ready output, and surfaces downturn-style signals in a repeatable way.

## Demo Steps

1. Open a terminal in `foundation-03`.
2. Run the MVP:

```powershell
python -m pipeline.run_pipeline
```

3. Confirm the generated artifacts:

```powershell
Get-Content data\transformed\gdp_transformed.json
Get-Content output\reports\pipeline_run_summary.md
```

## What to Point Out During the Demo

- The pipeline runs without external network access because sample mode is the default.
- Raw acquisition output is written to `data/raw/gdp_raw.json`.
- Transformed analytical output is written to `data/transformed/gdp_transformed.json`.
- The transformed dataset now includes:
  - `gdp_level`
  - `qoq_pct_change`
  - `yoy_pct_change`
  - `rolling_4q_change`
  - `signal_flag`
  - `signal_reasons`
- The markdown summary report highlights flagged periods and metric ranges.

## Optional Live Demo Path

If a valid FRED API key is available, set:

```powershell
$env:USE_LIVE_FRED="true"
$env:FRED_API_KEY="your_key_here"
$env:FRED_SERIES_ID="GDPC1"
python -m pipeline.run_pipeline
```

Use this path only if internet access and API credentials are available at demo time.
