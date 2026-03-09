import pandas as pd

from common import OUTPUT_DIR, get_logger

logger = get_logger("combine_metrics")


def classify_row(texas_quits_rate, national_quits_rate, rtp):
    if pd.isna(texas_quits_rate) or pd.isna(national_quits_rate) or pd.isna(rtp):
        return "Unknown"
    if texas_quits_rate >= national_quits_rate and rtp >= 1:
        return "High Pressure"
    if texas_quits_rate >= national_quits_rate:
        return "Elevated Pressure"
    if texas_quits_rate < national_quits_rate and rtp < 0:
        return "Below Benchmark"
    return "Watch"


def build_metrics(bls_path) -> pd.DataFrame:
    """
    Compute RTP and labels from processed BLS monthly data.
    """
    df = pd.read_csv(bls_path)

    required = [
        "period",
        "texas_quits_rate",
        "national_quits_rate",
        "market_heat_index",
    ]
    for col in required:
        if col not in df.columns:
            raise ValueError(f"Missing required column: {col}")

    df["rtp"] = (
        (df["texas_quits_rate"] - df["national_quits_rate"])
        * df["market_heat_index"]
    )

    df["risk_flag"] = df["rtp"].apply(
        lambda x: "HIGH" if pd.notna(x) and x >= 1.0 else "NORMAL"
    )

    df["quadrant"] = df.apply(
        lambda row: classify_row(
            row["texas_quits_rate"],
            row["national_quits_rate"],
            row["rtp"]
        ),
        axis=1
    )

    return df.sort_values(["year", "month"]).reset_index(drop=True)


def save_combined_output(df: pd.DataFrame):
    out_file = OUTPUT_DIR / "texas_national_radar.csv"
    out_file.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(out_file, index=False)
    logger.info(f"Saved combined metrics to {out_file}")
    return out_file


def run_combine_metrics(bls_path):
    df = build_metrics(bls_path)
    return save_combined_output(df)


if __name__ == "__main__":
    from common import PROCESSED_DIR
    bls_file = PROCESSED_DIR / "bls_texas_national_monthly.csv"
    run_combine_metrics(bls_file)