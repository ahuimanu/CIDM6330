Title: Foundation 3 MVP — Acquisition, Transformation, and Pipeline Integration

Summary:
This PR adds Foundation 3 work: a runnable acquisition module, transformation logic, pipeline runner (demo + real modes), unit tests, CI workflow, and documentation. It includes deterministic sample outputs for deliverables and updated AI collaboration notes.

Key changes (high level):
- Foundation3: `acquire.py`, `transform.py`, `pipeline.py`, `generate_sample.py`, `README.md`
- Tests: `Foundation3/tests/test_acquire.py`, `test_transform.py`, `test_transform_weights.py`
- Top-level runner: `run_pipeline.py` (CLI with `--start-date`, `--end-date`, `--demo`)
- Results: `Foundation3/results/transformed.json`, `pipeline.log` (sample outputs)
- CI: `.github/workflows/ci.yml` (runs Foundation3 tests only)
- Docs: `AI_LOG.MD` updated with Foundation 3 notes; `ARCHITECTURE.md` added.

How to run locally:
1. Create and activate the venv (optional):
   python -m venv .venv
   .\.venv\Scripts\activate
2. Install test deps:
   python -m pip install -r requirements-dev.txt
   (or at minimum: `pip install pytest`)
3. Demo run (no API key required):
   python run_pipeline.py --demo
   Output: `Foundation3/results/transformed.json`, `pipeline.log`.
4. Real run (requires FRED API key in env or .env):
   set FRED_API_KEY=your_key_here
   python run_pipeline.py --start-date 2018-01-01 --end-date 2023-01-01

Tests:
- Run: `python -m pytest Foundation3/tests`

Notes for reviewers:
- CI is scoped to Foundation3 tests to avoid unrelated repo tests.
- Tests mock network calls; CI does not require secrets.
- I included sample outputs under `Foundation3/results/` for inspection; remove them if you prefer not to include generated artifacts in repo.

Remaining / future work:
- Expand transformation tests for edge cases and final scoring formula.
- Add CI badge to README if desired.

If you want, I can open the PR on your remote (requires repo permissions/token). Otherwise push the branch and open a PR from `feature/foundation3-mvp` to your main branch.
