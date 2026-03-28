# Foundation 3 — MVP Iterations

This folder contains starter code for Foundation 3 MVPs: acquisition, transformation, and a small pipeline runner.

Quick start

1. Create a `.env` file in the repository root with your FRED API key:

```
FRED_API_KEY=your_api_key_here
```

2. Run the pipeline (writes CSVs and `transformed.json` into `Foundation3/results/`):

```powershell
python run_pipeline.py
```

Notes
- Tests mock external calls; running tests does not require a real FRED API key.
- The code is intentionally small and focused; extend transformation logic in `transform.py` to match your final scoring formula.
 
 Results and logs
 - Demo or real-run artifacts are written to `Foundation3/results/`:
	 - `combined.csv` — combined raw series
	 - `transformed.json` — transformed rows with `S_score` and `Recommendation`
	 - `pipeline.log` — pipeline run log (demo mode writes this)

CI
- This repository includes a GitHub Actions workflow at `.github/workflows/ci.yml` that runs `pytest` on push and pull requests. Tests mock network calls so CI does not require `FRED_API_KEY`.

CLI
- Use `run_pipeline.py` to run the pipeline with CLI arguments:

```powershell
python run_pipeline.py --start-date 2020-01-01 --end-date 2023-01-01
python run_pipeline.py --demo  # force demo synthetic run
```

