from pathlib import Path
import sys
import logging
import pandas as pd

# ensure repository root is on sys.path so package imports work when running script
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from Foundation3.transform import transform_combined


def make_synthetic_data(out_dir: Path):
    out_dir.mkdir(parents=True, exist_ok=True)
    idx = pd.to_datetime(["2021-01-31", "2021-02-28", "2021-03-31", "2021-04-30", "2021-05-31"])
    data = {
        "IPG3344S": [100.0, 105.0, 110.25, 115.7625, 121.5506],
        "CAPUTLG3344SQ": [70.0, 71.4, 72.828, 74.28456, 75.7732512],
        "A34STI": [50.0, 52.5, 55.125, 57.88125, 60.7753125],
        "PCU334413334413": [200.0, 198.0, 197.01, 196.0399, 195.079501],
    }
    df = pd.DataFrame(data, index=idx)
    combined_csv = out_dir / "combined.csv"
    df.to_csv(combined_csv)
    return df


def main():
    out = Path(__file__).parent / "results"
    log_file = out / "pipeline.log"
    out.mkdir(parents=True, exist_ok=True)

    logging.basicConfig(level=logging.INFO, filename=log_file, filemode="w",
                        format="%(asctime)s %(levelname)s %(message)s")
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
