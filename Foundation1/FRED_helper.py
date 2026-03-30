from pathlib import Path
import os
from typing import Optional, Dict
import requests
import pandas as pd
from dotenv import load_dotenv

# explicitly load .env from repo root (two levels up from this file)
dotenv_path = Path(__file__).resolve().parents[1] / ".env"
load_dotenv(dotenv_path=dotenv_path)

FRED_BASE = "https://api.stlouisfed.org/fred/series/observations"
DEFAULT_TIMEOUT = 20


def get_api_key() -> str:
    key = os.getenv("FRED_API_KEY")
    if key:
        key = key.strip()
    if not key:
        raise RuntimeError("FRED_API_KEY not set in env or .env")
    return key


def get_fred_series(
    series_id: str,
    api_key: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    file_type: str = "json",
    extra: Optional[Dict] = None,
) -> pd.DataFrame:
    api_key = api_key or get_api_key()
    params = {
        "series_id": series_id,
        "api_key": api_key,
        "file_type": file_type,
    }
    if start_date:
        params["start_date"] = start_date
    if end_date:
        params["end_date"] = end_date
    if extra:
        params.update(extra)

    with requests.Session() as s:
        r = s.get(FRED_BASE, params=params, timeout=DEFAULT_TIMEOUT)
        r.raise_for_status()

    if file_type == "json":
        payload = r.json()
        obs = payload.get("observations", [])
        if not obs:
            return pd.DataFrame()
        df = pd.DataFrame(obs)
        df["value"] = pd.to_numeric(df["value"].replace(".", pd.NA))
        df["date"] = pd.to_datetime(df["date"])
        return df.set_index("date").sort_index()
    else:
        from io import StringIO

        return pd.read_csv(StringIO(r.text), parse_dates=["date"]).set_index("date")
