from common import RAW_DIR, PROCESSED_DIR, get_logger
from config import START_YEAR, END_YEAR, ALERT_THRESHOLD
from fetch_bls import run_fetch_bls
from transform_bls import run_transform_bls
from combine_metrics import run_combine_metrics
from validate_alerts import run_validate_alerts

logger = get_logger("run_pipeline")


def run_pipeline(start_year: int, end_year: int, alert_threshold: float = 1.0):
    """
    Run the full BLS Texas + National pipeline.
    """
    logger.info("Starting Texas + National BLS pipeline")

    raw_bls = run_fetch_bls(start_year, end_year)
    processed_bls = run_transform_bls(raw_bls)
    combined_output = run_combine_metrics(processed_bls)
    alerts_output = run_validate_alerts(combined_output, threshold=alert_threshold)

    logger.info("Pipeline finished successfully")

    return {
        "raw_bls": raw_bls,
        "processed_bls": processed_bls,
        "combined_output": combined_output,
        "alerts_output": alerts_output,
    }


if __name__ == "__main__":
    outputs = run_pipeline(
        start_year=START_YEAR,
        end_year=END_YEAR,
        alert_threshold=ALERT_THRESHOLD,
    )
    print(outputs)