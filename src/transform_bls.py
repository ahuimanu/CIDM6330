import pandas as pd

from common import PROCESSED_DIR, get_logger, load_json
from config import BLS_SERIES

logger = get_logger("transform_bls")

SERIES_NAMES = {
    BLS_SERIES["texas_quits_rate"]: "texas_quits_rate",
    BLS_SERIES["texas_openings_rate"]: "texas_openings_rate",
    BLS_SERIES["texas_hires_rate"]: "texas_hires_rate",
    BLS_SERIES["national_quits_rate"]: "national_quits_rate",
}


def transform_bls(raw_data: dict, series_names: dict | None = None) -> pd.DataFrame:
    """
    Transform raw BLS JSON into monthly Texas + National comparison data.
    """
    if series_names is None:
        series_names = SERIES_NAMES

    rows = []

    for series in raw_data.get("Results", {}).get("series", []):
        series_id = series.get("seriesID")
        metric = series_names.get(series_id, series_id)

        for item in series.get("data", []):
            period = item.get("period", "")
            if not period.startswith("M"):
                continue

            try:
                rows.append(
                    {
                        "year": int(item["year"]),
                        "month": int(period[1:]),
                        "metric": metric,
                        "value": float(item["value"]),
                    }
                )
            except Exception:
                logger.warning(f"Skipping bad BLS row: {item}")

    df = pd.DataFrame(rows)

    if df.empty:
        raise ValueError("No usable BLS data found")

    df = df.pivot_table(
        index=["year", "month"],
        columns="metric",
        values="value",
        aggfunc="first"
    ).reset_index()

    df.columns.name = None
    df["period"] = df["year"].astype(str) + "-" + df["month"].astype(str).str.zfill(2)

    required = [
        "texas_quits_rate",
        "texas_openings_rate",
        "texas_hires_rate",
        "national_quits_rate",
    ]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing expected BLS field: {col}")

    df["market_heat_index"] = df["texas_openings_rate"] / df["texas_hires_rate"]
    df.loc[df["texas_hires_rate"] == 0, "market_heat_index"] = None

    return df.sort_values(["year", "month"]).reset_index(drop=True)


def save_bls_processed(df: pd.DataFrame):
    out_file = PROCESSED_DIR / "bls_texas_national_monthly.csv"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_file, index=False)
    logger.info(f"Saved processed BLS data to {out_file}")
    return out_file


def run_transform_bls(raw_file_path):
    raw_data = load_json(raw_file_path)
    df = transform_bls(raw_data)
    return save_bls_processed(df)


if __name__ == "__main__":
    from common import RAW_DIR
    from config import START_YEAR, END_YEAR

    raw_file = RAW_DIR / "bls" / f"bls_raw_{START_YEAR}_{END_YEAR}.json"
    run_transform_bls(raw_file)