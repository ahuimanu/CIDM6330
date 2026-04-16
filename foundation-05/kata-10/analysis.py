"""
Kata 10 -- GDP Analysis module (built via TDD).

Functions are added one TDD cycle at a time:
  Cycle 1: detect_contractions
  Cycle 2: compute_peak_trough  (+ PeakTrough dataclass)
  Cycle 3: generate_summary_report
"""

import sqlite3
from pathlib import Path


def detect_contractions(db_path: Path) -> list[str]:
    with sqlite3.connect(db_path) as conn:
        rows = conn.execute(
            "SELECT date FROM gdp_observations WHERE growth_rate < 0 ORDER BY date"
        ).fetchall()
    return [r[0] for r in rows]
