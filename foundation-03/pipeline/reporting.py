def _format_optional_number(value, suffix=""):
    if value is None:
        return "n/a"
    return f"{value:.4f}{suffix}"


def build_run_summary(
    *,
    live_mode,
    series_id,
    observation_start,
    observation_end,
    raw_payload,
    transformed_rows,
    raw_file,
    transformed_file,
):
    qoq_values = [
        row["qoq_pct_change"]
        for row in transformed_rows
        if row.get("qoq_pct_change") is not None
    ]
    yoy_values = [
        row["yoy_pct_change"]
        for row in transformed_rows
        if row.get("yoy_pct_change") is not None
    ]
    flagged_rows = [row for row in transformed_rows if row.get("signal_flag")]

    lines = [
        "# Pipeline Run Summary",
        f"- Live mode: {live_mode}",
        f"- Series: {series_id}",
        f"- Observation start: {observation_start or 'default'}",
        f"- Observation end: {observation_end or 'default'}",
        f"- Raw observations: {len(raw_payload.get('observations', []))}",
        f"- Transformed records: {len(transformed_rows)}",
        f"- Flagged periods: {len(flagged_rows)}",
        f"- Raw file: {raw_file}",
        f"- Transformed file: {transformed_file}",
        "",
        "## Derived Metrics",
        f"- QoQ change min: {_format_optional_number(min(qoq_values), '%') if qoq_values else 'n/a'}",
        f"- QoQ change max: {_format_optional_number(max(qoq_values), '%') if qoq_values else 'n/a'}",
        f"- YoY change min: {_format_optional_number(min(yoy_values), '%') if yoy_values else 'n/a'}",
        f"- YoY change max: {_format_optional_number(max(yoy_values), '%') if yoy_values else 'n/a'}",
        "",
        "## Flagged Periods",
    ]

    if not flagged_rows:
        lines.append("- None")
    else:
        for row in flagged_rows:
            reasons = ", ".join(row.get("signal_reasons", [])) or "unspecified"
            lines.append(
                f"- {row['date']}: qoq={_format_optional_number(row['qoq_pct_change'], '%')}, "
                f"yoy={_format_optional_number(row['yoy_pct_change'], '%')}, reasons={reasons}"
            )

    return "\n".join(lines)
