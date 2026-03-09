import time
import requests

from common import RAW_DIR, get_logger, save_json
from config import BLS_SERIES

logger = get_logger("fetch_bls")

BLS_URL = "https://api.bls.gov/publicAPI/v2/timeseries/data/"


def fetch_bls(start_year: int, end_year: int, series_map: dict | None = None) -> dict:
    """
    Fetch raw BLS JOLTS data for Texas + National comparison.
    """
    if series_map is None:
        series_map = BLS_SERIES

    payload = {
        "seriesid": list(series_map.values()),
        "startyear": str(start_year),
        "endyear": str(end_year),
    }

    for attempt in range(3):
        try:
            response = requests.post(BLS_URL, json=payload, timeout=30)

            if response.status_code == 429:
                logger.warning("BLS rate limit hit. Retrying...")
                time.sleep(2 * (attempt + 1))
                continue

            response.raise_for_status()
            data = response.json()

            if data.get("status") != "REQUEST_SUCCEEDED":
                raise ValueError(f"BLS request failed: {data}")

            return data

        except Exception as e:
            logger.warning(f"BLS fetch attempt {attempt + 1} failed: {e}")
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))


def save_bls_raw(data: dict, start_year: int, end_year: int):
    out_file = RAW_DIR / "bls" / f"bls_raw_{start_year}_{end_year}.json"
    save_json(out_file, data)
    logger.info(f"Saved BLS raw data to {out_file}")
    return out_file


def run_fetch_bls(start_year: int, end_year: int):
    data = fetch_bls(start_year, end_year)
    return save_bls_raw(data, start_year, end_year)


if __name__ == "__main__":
    from config import START_YEAR, END_YEAR
    run_fetch_bls(START_YEAR, END_YEAR)