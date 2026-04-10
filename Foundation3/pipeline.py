import logging
from pathlib import Path

import pandas as pd

from Foundation3.acquire import fetch_all
from Foundation3.transform import transform_combined

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


ASYMMETRIC_WEIGHTS = {
    "IPG3344S": 1.0,       # Industrial Production — positive supply signal
    "CAPUTLG3344SQ": 1.0,  # Capacity Utilization — positive supply signal
    "A34STI": 1.0,         # Inventory — positive supply signal
    "PCU334413334413": -1.0,  # PPI — rising prices are a bad supply signal (Risk 7)
}


def run_pipeline(series_list, out_dir: Path, start_date=None, end_date=None):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Starting pipeline for %d series", len(series_list))
    frames = fetch_all(series_list, out_dir, start_date=start_date, end_date=end_date)
    if not frames:
        logger.error("No data fetched; aborting pipeline")
        return

    # Risk 5: verify all requested series were fetched before proceeding
    missing = [s for s in series_list if s not in frames]
    if missing:
        logger.warning("Missing series (discontinued or fetch failed): %s", missing)

    # Risk 8: build combined DataFrame directly from returned frames instead of
    # re-reading combined.csv (avoids silent stale-file scenario on disk-full).
    df = pd.concat(frames.values(), axis=1)
    logger.info("Combined DataFrame shape: %s", df.shape)

    # Risk 7: apply asymmetric weights so PPI contribution is negative
    weights = {s: ASYMMETRIC_WEIGHTS.get(s, 1.0) for s in df.columns}
    transformed = transform_combined(df, weights=weights)
    if transformed.empty:
        logger.error("Transformed output empty; check inputs")
        return

    out_json = out_dir / "transformed.json"
    transformed.reset_index().to_json(out_json, orient="records", date_format="iso")
    logger.info(
        "Wrote transformed artifacts to %s (rows=%d, cols=%d)",
        out_json,
        transformed.shape[0],
        transformed.shape[1],
    )
    return out_json


if __name__ == "__main__":
    SERIES = ["IPG3344S", "CAPUTLG3344SQ", "A34STI", "PCU334413334413"]
    out = Path(__file__).parent / "results"
    run_pipeline(SERIES, out)
