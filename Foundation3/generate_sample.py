import logging
import sys
from pathlib import Path

import pandas as pd

# ensure repository root is on sys.path so package imports work when running script
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Foundation3.transform import transform_combined


def make_synthetic_data(out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    # Scenario: production and capacity decline while inventories fall and prices
    # rise — a contraction pattern that should trigger an OVERBUY recommendation.
    idx = pd.to_datetime(
        ["2021-01-31", "2021-02-28", "2021-03-31", "2021-04-30", "2021-05-31"]
    )
    data = {
        "IPG3344S": [100.0, 97.0, 94.09, 91.27, 88.53],  # -3% per month
        "CAPUTLG3344SQ": [70.0, 68.6, 67.23, 65.88, 64.56],  # -2% per month
        "A34STI": [50.0, 48.5, 47.05, 45.63, 44.26],  # -3% (inventories draining)
        "PCU334413334413": [200.0, 204.0, 208.08, 212.24, 216.48],  # +2% (prices up)
    }
    df = pd.DataFrame(data, index=idx)
    combined_csv = out_dir / "combined.csv"
    df.to_csv(combined_csv)
    return df


def main():
    out = Path(__file__).parent / "results"
    log_file = out / "pipeline.log"
    out.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        filename=log_file,
        filemode="w",
        format="%(asctime)s %(levelname)s %(message)s",
    )
    logger = logging.getLogger("foundation3.sample")

    logger.info("Generating synthetic data and running transform")
    df = make_synthetic_data(out)

    transformed = transform_combined(df)
    if transformed.empty:
        logger.error("Transformed output empty")
        return

    out_json = out / "transformed.json"
    transformed.reset_index().to_json(out_json, orient="records", date_format="iso")
    logger.info("Wrote transformed.json to %s", out_json)
    print("Sample generated:", out_json)


if __name__ == "__main__":
    main()
