"""
Kata 10 -- GDP Analysis module (built via TDD).

Functions are added one TDD cycle at a time:
  Cycle 1: detect_contractions
  Cycle 2: compute_peak_trough  (+ PeakTrough dataclass)
  Cycle 3: generate_summary_report
"""

import sqlite3
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class PeakTrough:
    """Immutable container for the peak and trough of a GDP series."""

    peak_date: str
    peak_value: float
    trough_date: str
    trough_value: float


_CONTRACTIONS_SQL = (
    "SELECT date FROM gdp_observations WHERE growth_rate < 0 ORDER BY date"
)


def detect_contractions(db_path: Path) -> list[str]:
    """Return ISO-date strings for every quarter where GDP fell (growth_rate < 0).

    Results are sorted chronologically.  An empty list means no contractions
    were found (or the database has fewer than two rows so no rates exist yet).
    """
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(_CONTRACTIONS_SQL).fetchall()
    return [r[0] for r in rows]

def compute_peak_trough(db_path: Path) -> PeakTrough:
    """Return the date and value of the highest and lowest GDP observations."""
    with sqlite3.connect(db_path) as conn:
        peak_date, peak_value = conn.execute(
            "SELECT date, value FROM gdp_observations ORDER BY value DESC LIMIT 1"
        ).fetchone()
        trough_date, trough_value = conn.execute(
            "SELECT date, value FROM gdp_observations ORDER BY value ASC LIMIT 1"
        ).fetchone()
    return PeakTrough(
        peak_date=peak_date,
        peak_value=peak_value,
        trough_date=trough_date,
        trough_value=trough_value,
    )


def generate_summary_report(db_path: Path, report_path: Path) -> None:
    contractions = detect_contractions(db_path)
    pt = compute_peak_trough(db_path)
    lines = ["# GDP Analysis Summary\n", "\n## Contractions\n"]
    for d in contractions:
        lines.append(f"- {d}\n")
    if not contractions:
        lines.append("- None detected\n")
    lines.append(f"\n## Peak\n- **{pt.peak_date}**: {pt.peak_value:.2f}\n")
    lines.append(f"\n## Trough\n- **{pt.trough_date}**: {pt.trough_value:.2f}\n")
    report_path.write_text("".join(lines), encoding="utf-8")
