from pathlib import Path
import os


def _to_bool(value, default=False):
	if value is None:
		return default
	return str(value).strip().lower() in {"1", "true", "yes", "on"}


def _to_int(value, default):
	try:
		return int(value)
	except (TypeError, ValueError):
		return default


def _to_float(value, default):
	try:
		return float(value)
	except (TypeError, ValueError):
		return default

BASE_DIR = Path(__file__).resolve().parents[1]
RAW_DIR = BASE_DIR / "data" / "raw"
TRANSFORMED_DIR = BASE_DIR / "data" / "transformed"
REPORT_DIR = BASE_DIR / "output" / "reports"

RAW_FILE = RAW_DIR / "gdp_raw.json"
TRANSFORMED_FILE = TRANSFORMED_DIR / "gdp_transformed.json"

FRED_API_KEY = os.getenv("FRED_API_KEY", "")
FRED_SERIES_ID = os.getenv("FRED_SERIES_ID", "GDPC1")
FRED_BASE_URL = "https://api.stlouisfed.org/fred/series/observations"
FRED_OBSERVATION_START = os.getenv("FRED_OBSERVATION_START", "")
FRED_OBSERVATION_END = os.getenv("FRED_OBSERVATION_END", "")

USE_LIVE_FRED = _to_bool(os.getenv("USE_LIVE_FRED"), default=False)
FRED_REQUEST_TIMEOUT_SECONDS = _to_int(os.getenv("FRED_REQUEST_TIMEOUT_SECONDS"), default=15)
FRED_MAX_RETRIES = _to_int(os.getenv("FRED_MAX_RETRIES"), default=2)
FRED_RETRY_BACKOFF_SECONDS = _to_float(os.getenv("FRED_RETRY_BACKOFF_SECONDS"), default=1.0)
FRED_FALLBACK_TO_SAMPLE_ON_ERROR = _to_bool(os.getenv("FRED_FALLBACK_TO_SAMPLE_ON_ERROR"), default=True)
