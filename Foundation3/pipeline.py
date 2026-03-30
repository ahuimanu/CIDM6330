from pathlib import Path
import json
import logging

from Foundation3.acquire import fetch_all
from Foundation3.transform import transform_combined

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def run_pipeline(series_list, out_dir: Path, start_date=None, end_date=None):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    logger.info("Starting pipeline for %d series", len(series_list))
    frames = fetch_all(series_list, out_dir, start_date=start_date, end_date=end_date)
    if not frames:
        logger.error("No data fetched; aborting pipeline")
        return

    combined = out_dir / "combined.csv"
    import pandas as pd

    df = pd.read_csv(combined, parse_dates=[0], index_col=0)
    logger.info("Read combined CSV with shape %s", df.shape)

    transformed = transform_combined(df)
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
