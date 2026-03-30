from pathlib import Path
import logging
import time
from typing import List, Dict, Optional

import pandas as pd

from Foundation1.FRED_helper import get_fred_series

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def fetch_all(
    series_list: List[str],
    out_dir: Path,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    retries: int = 2,
    backoff: float = 1.5,
) -> Dict[str, pd.Series]:
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    frames: Dict[str, pd.Series] = {}

    for s in series_list:
        logger.info("Fetching %s", s)
        attempt = 0
        last_exc = None
        while attempt <= retries:
            try:
                df = get_fred_series(s, start_date=start_date, end_date=end_date)
                if df.empty:
                    logger.warning("No data returned for %s", s)
                    break
                (out_dir / f"{s}.csv").write_text(df.to_csv())
                frames[s] = df["value"].rename(s)
                logger.info("Fetched %s (%d rows)", s, len(df))
                break
            except Exception as e:
                last_exc = e
                attempt += 1
                logger.warning("Attempt %d failed for %s: %s", attempt, s, e)
                # log exception traceback at debug level
                logger.debug("Exception details", exc_info=e)
                time.sleep(backoff * attempt)
        else:
            logger.error(
                "Failed to fetch %s after %d attempts: %s", s, retries + 1, last_exc
            )
            logger.debug("Final exception for %s", s, exc_info=last_exc)

    if not frames:
        logger.error("No series fetched; nothing to save")
        return {}

    combined = pd.concat(frames.values(), axis=1)
    combined.to_csv(out_dir / "combined.csv")
    logger.info("Saved combined CSV to %s", out_dir / "combined.csv")
    return frames


if __name__ == "__main__":
    # default series chosen from Foundation2 Data_Pipeline notes
    SERIES = [
        "IPG3344S",
        "CAPUTLG3344SQ",
        "A34STI",
        "PCU334413334413",
    ]
    out = Path(__file__).parent / "results"
    fetch_all(SERIES, out)
