import argparse
import json
import os
import random
import time
from pathlib import Path

try:
    import requests
except ModuleNotFoundError:
    class _RequestsFallback:
        class RequestException(Exception):
            pass

        class HTTPError(RequestException):
            def __init__(self, message: str, response=None):
                super().__init__(message)
                self.response = response

        class Timeout(RequestException):
            pass

        @staticmethod
        def get(*_args, **_kwargs):
            raise ModuleNotFoundError(
                "requests is required for live API calls but is not installed"
            )

    requests = _RequestsFallback()

BASE_URL = "https://api.stlouisfed.org/fred/series/observations"


def request_with_backoff(
    params: dict[str, str],
    retries: int = 5,
    backoff_base_seconds: float = 0.75,
    timeout_seconds: int = 30,
) -> dict:
    last_error: Exception | None = None

    for attempt in range(retries + 1):
        try:
            response = requests.get(BASE_URL, params=params, timeout=timeout_seconds)

            if response.status_code in (429, 500, 502, 503, 504):
                raise requests.HTTPError(
                    f"Transient HTTP {response.status_code}", response=response
                )

            response.raise_for_status()
            return response.json()
        except (requests.RequestException, ValueError) as exc:
            last_error = exc
            if attempt >= retries:
                break

            sleep_seconds = min(backoff_base_seconds * (1.75**attempt), 25)
            jitter = random.uniform(0.05, 0.30 * sleep_seconds)
            time.sleep(sleep_seconds + jitter)

    raise RuntimeError(
        f"Request failed after {retries} retries: {last_error}"
    ) from last_error


def fetch_all_observations(
    api_key: str,
    series_id: str,
    page_size: int = 1000,
    max_pages: int | None = None,
) -> list[dict]:
    all_observations: list[dict] = []
    offset = 0
    pages_fetched = 0

    while True:
        params = {
            "api_key": api_key,
            "series_id": series_id,
            "file_type": "json",
            "sort_order": "asc",
            "limit": str(page_size),
            "offset": str(offset),
        }

        payload = request_with_backoff(params=params)
        observations = payload.get("observations", [])
        total_count = int(payload.get("count", 0))

        if not observations:
            break

        all_observations.extend(observations)
        pages_fetched += 1
        offset += page_size

        if max_pages is not None and pages_fetched >= max_pages:
            break

        if len(all_observations) >= total_count:
            break

    return all_observations


def save_output(output_path: Path, series_id: str, rows: list[dict]) -> None:
    output_path.parent.mkdir(parents=True, exist_ok=True)
    result = {
        "series_id": series_id,
        "record_count": len(rows),
        "fetched_at_unix": int(time.time()),
        "observations": rows,
    }
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Kata 3: FRED API consumption with pagination, retries, "
            "and output file"
        )
    )
    parser.add_argument(
        "--series-id", default="GDP", help="FRED series id (default: GDP)"
    )
    parser.add_argument("--page-size", type=int, default=1000, help="Records per page")
    parser.add_argument(
        "--max-pages", type=int, default=None, help="Optional page cap for testing"
    )
    parser.add_argument(
        "--output",
        default="output/gdp_observations.json",
        help="Path for output JSON",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    api_key = os.getenv("FRED_API_KEY")

    if not api_key:
        raise SystemExit("Missing FRED_API_KEY environment variable")

    rows = fetch_all_observations(
        api_key=api_key,
        series_id=args.series_id,
        page_size=args.page_size,
        max_pages=args.max_pages,
    )

    save_output(Path(args.output), args.series_id, rows)
    print(f"Saved {len(rows)} records to {args.output}")


if __name__ == "__main__":
    main()
