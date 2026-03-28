# Running `Foundation3.acquire`

From the repository root (recommended):

1. Install dependencies if needed:

```bash
pip install -r requirements.txt
```

2. Ensure `FRED_API_KEY` is available — either in a repo-root `.env` file or set in your shell.

3. Run the module from the repo root:

```bash
python -m Foundation3.acquire
```

Notes:
- Output files are written to the `Foundation3/results` folder.
- On Windows PowerShell you can set the key with:

```powershell
$env:FRED_API_KEY = "your_key_here"
python -m Foundation3.acquire
```
