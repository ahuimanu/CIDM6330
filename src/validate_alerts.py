import pandas as pd

from common import OUTPUT_DIR, get_logger

logger = get_logger("validate_alerts")


def validate_alerts(df: pd.DataFrame, threshold: float = 1.0) -> pd.DataFrame:
    df = df.copy()
    df["alert"] = df["rtp"].apply(
        lambda x: "TRIGGER" if pd.notna(x) and x >= threshold else "NONE"
    )
    df["alert_reason"] = df["rtp"].apply(
        lambda x: f"RTP exceeded threshold {threshold}"
        if pd.notna(x) and x >= threshold else ""
    )
    return df


def save_alerts(df: pd.DataFrame):
    out_file = OUTPUT_DIR / "texas_national_alerts.csv"
    df.to_csv(out_file, index=False)
    logger.info(f"Saved alerts to {out_file}")
    return out_file


def run_validate_alerts(input_file, threshold: float = 1.0):
    df = pd.read_csv(input_file)
    alerts = validate_alerts(df, threshold=threshold)
    return save_alerts(alerts)


if __name__ == "__main__":
    from common import OUTPUT_DIR
    from config import ALERT_THRESHOLD

    input_file = OUTPUT_DIR / "texas_national_radar.csv"
    run_validate_alerts(input_file, threshold=ALERT_THRESHOLD)