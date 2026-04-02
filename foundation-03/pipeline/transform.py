import json
from datetime import datetime
from pathlib import Path


def _parse_iso_date(date_text):
    return datetime.strptime(date_text, "%Y-%m-%d")


def _pct_change(current, previous):
    if previous in (None, 0):
        return None
    return round(((current - previous) / previous) * 100, 4)


def transform_observations(raw_payload):
    observations = raw_payload.get("observations", [])
    cleaned = []
    seen_dates = set()

    for item in observations:
        value = item.get("value")
        date = item.get("date")

        if date is None or value in (None, "."):
            continue

        try:
            parsed_date = _parse_iso_date(date)
            numeric_value = float(value)
        except (TypeError, ValueError):
            continue

        if date in seen_dates:
            continue

        seen_dates.add(date)
        cleaned.append({"date": date, "value": numeric_value, "_sort_date": parsed_date})

    cleaned.sort(key=lambda row: row["_sort_date"])

    transformed = []
    for index, row in enumerate(cleaned):
        current_value = row["value"]
        previous_value = cleaned[index - 1]["value"] if index >= 1 else None
        prior_year_value = cleaned[index - 4]["value"] if index >= 4 else None
        previous_qoq = transformed[index - 1]["qoq_pct_change"] if index >= 1 else None

        qoq_pct_change = _pct_change(current_value, previous_value)
        yoy_pct_change = _pct_change(current_value, prior_year_value)
        rolling_4q_change = (
            round(current_value - prior_year_value, 4) if prior_year_value is not None else None
        )

        signal_reasons = []
        if qoq_pct_change is not None and qoq_pct_change < 0:
            signal_reasons.append("negative_qoq_growth")
        if previous_qoq is not None and qoq_pct_change is not None and qoq_pct_change < previous_qoq:
            signal_reasons.append("growth_slowdown")
        if yoy_pct_change is not None and yoy_pct_change < 0:
            signal_reasons.append("negative_yoy_growth")

        transformed.append(
            {
                "date": row["date"],
                "gdp_level": current_value,
                "qoq_pct_change": qoq_pct_change,
                "yoy_pct_change": yoy_pct_change,
                "rolling_4q_change": rolling_4q_change,
                "signal_flag": bool(signal_reasons),
                "signal_reasons": signal_reasons,
            }
        )

    return transformed


def save_transformed_data(rows, path: Path):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as file:
        json.dump(rows, file, indent=2)
