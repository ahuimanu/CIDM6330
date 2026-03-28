# Kata7 artifacts

This folder contains artifacts produced while completing Kata7 (testing + pre-commit hooks).

- `junit.xml` — pytest JUnit-style test results
- `coverage_html/` — HTML coverage report for `Katas/Kata4`
- `report.md` — sample pipeline report generated from a small sample DB
- `generate_report.py` — helper script that creates a sample DB and writes `report.md`

Run locally:

1. Activate the virtual environment: `.venv\Scripts\Activate.ps1`
2. Run tests and produce artifacts:
   python -m pytest Katas/Kata4 --junitxml=Katas/Kata7/junit.xml --cov=Katas/Kata4 --cov-report=html:Katas/Kata7/coverage_html -q
3. Generate sample pipeline report:
   python Katas/Kata7/generate_report.py
