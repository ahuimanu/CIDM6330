from pathlib import Path

from .acquire import fetch_gdp_observations, save_raw_payload
from .config import (
    FRED_OBSERVATION_END,
    FRED_OBSERVATION_START,
    FRED_SERIES_ID,
    RAW_FILE,
    REPORT_DIR,
    TRANSFORMED_FILE,
    USE_LIVE_FRED,
)
from .logging_config import get_logger
from .reporting import build_run_summary
from .transform import save_transformed_data, transform_observations


def run_pipeline(use_live=None):
    logger = get_logger()
    live_mode = USE_LIVE_FRED if use_live is None else use_live
    logger.info("Starting GDP pipeline")

    raw_payload = fetch_gdp_observations(
        use_live=live_mode,
        series_id=FRED_SERIES_ID,
        observation_start=FRED_OBSERVATION_START or None,
        observation_end=FRED_OBSERVATION_END or None,
    )
    save_raw_payload(raw_payload, RAW_FILE)
    logger.info("Raw data saved to %s", RAW_FILE)

    transformed = transform_observations(raw_payload)
    save_transformed_data(transformed, TRANSFORMED_FILE)
    logger.info("Transformed data saved to %s", TRANSFORMED_FILE)

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / "pipeline_run_summary.md"
    report_path.write_text(
        build_run_summary(
            live_mode=live_mode,
            series_id=FRED_SERIES_ID,
            observation_start=FRED_OBSERVATION_START,
            observation_end=FRED_OBSERVATION_END,
            raw_payload=raw_payload,
            transformed_rows=transformed,
            raw_file=RAW_FILE,
            transformed_file=TRANSFORMED_FILE,
        ),
        encoding="utf-8",
    )
    logger.info("Run summary written to %s", report_path)

    return {
        "raw_count": len(raw_payload.get("observations", [])),
        "transformed_count": len(transformed),
        "flagged_count": len([row for row in transformed if row.get("signal_flag")]),
        "raw_file": str(RAW_FILE),
        "transformed_file": str(TRANSFORMED_FILE),
        "report_file": str(report_path),
    }


if __name__ == "__main__":
    run_pipeline()
