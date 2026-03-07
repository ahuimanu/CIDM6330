# Reproducible Steps for Foundation1

Follow these exact steps to reproduce the data retrieval and the lag test used in Foundation 1.

1. Add your FRED API key to a `.env` file at the repository root with the variable `FRED_API_KEY`:

   FRED_API_KEY=your_api_key_here

2. Activate the project's virtual environment (PowerShell):

```powershell
& .venv\Scripts\Activate.ps1
```

3. Install dependencies (if needed):

```powershell
pip install -r CIDM6330/requirements.txt
```

4. Run the full fetch to store series CSVs in `CIDM6330/Foundation1/fred_data`:

```powershell
python CIDM6330/Foundation1/FRED_fetch.py
```

5. Run the lag test to compute leading-lag correlations between `IPG3344S` and `CPIAUCSL`:

```powershell
python CIDM6330/Foundation1/lag_test.py
```

Outputs:
- `CIDM6330/Foundation1/fred_data/combined.csv` (combined series)
- `CIDM6330/Foundation1/fred_data/lag_results.json` (lag correlation results)

If you run into module import errors, ensure your working directory is the repository root and the virtual environment is active.