"""
Kata 10 -- GDP Analysis module (built via TDD).

Functions are added one TDD cycle at a time:
  Cycle 1: detect_contractions
  Cycle 2: compute_peak_trough  (+ PeakTrough dataclass)
  Cycle 3: generate_summary_report
"""

import sqlite3
from pathlib import Path


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

def compute_peak_trough(db_path: Path):  # type: ignore[return]
    with sqlite3.connect(db_path) as conn:
        peak = conn.execute(
            "SELECT date, value FROM gdp_observations ORDER BY value DESC LIMIT 1"
        ).fetchone()
        trough = conn.execute(
            "SELECT date, value FROM gdp_observations ORDER BY value ASC LIMIT 1"
        ).fetchone()
    from collections import namedtuple
    PT = namedtuple("PeakTrough", ["peak_date", "peak_value", "trough_date", "trough_value"])
    return PT(peak[0], peak[1], trough[0], trough[1])
