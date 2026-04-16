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


def _contractions_section(dates: list[str]) -> str:
    """Render the Contractions section as a Markdown string."""
    if not dates:
        return "\n## Contractions\n- None detected\n"
    items = "".join(f"- {d}\n" for d in dates)
    return f"\n## Contractions\n{items}"


def generate_summary_report(db_path: Path, report_path: Path) -> None:
    """Write a Markdown GDP analysis summary to *report_path*.

    Sections: title, contractions list, peak observation, trough observation.
    """
    contractions = detect_contractions(db_path)
    pt = compute_peak_trough(db_path)
    content = (
        "# GDP Analysis Summary\n"
        + _contractions_section(contractions)
        + f"\n## Peak\n- **{pt.peak_date}**: {pt.peak_value:.2f}\n"
        + f"\n## Trough\n- **{pt.trough_date}**: {pt.trough_value:.2f}\n"
    )
    report_path.write_text(content, encoding="utf-8")
