from pathlib import Path
import pandas as pd
from typing import Dict, Optional


def transform_combined(
    combined: pd.DataFrame,
    weights: Optional[Dict[str, float]] = None,
    threshold: float = 0.0,
) -> pd.DataFrame:
    """Transform combined raw series into rolling metrics and an `S_score`.

    Steps:
    - compute month-over-month percent change for each series
    - compute 3-month rolling mean of percent changes
    - compute `S_score` as a weighted average of rolling metrics (equal weights by default)
    - add `Recommendation`: 'OVERBUY' when `S_score` > `threshold`, else 'HOLD'

    Args:
        combined: wide DataFrame of raw series (columns are series ids, index is datetime)
        weights: optional mapping of column -> weight (missing keys treated as 0)
        threshold: numeric threshold to decide recommendation

    Returns:
        DataFrame containing the rolling metrics, `S_score`, and `Recommendation`.
    """
    if combined is None or combined.empty:
        return pd.DataFrame()

    pct = combined.pct_change()
    pct = pct.dropna(how="all")

    rolling = pct.rolling(3).mean()
    rolling = rolling.dropna(how="all")

    if rolling.empty:
        return pd.DataFrame()

    cols = list(rolling.columns)

    if weights:
        # build weight Series aligned to columns
        w = pd.Series({c: float(weights.get(c, 0.0)) for c in cols})
        total = w.sum()
        if total == 0:
            # fallback to equal weights
            s = rolling.mean(axis=1)
        else:
            s = (rolling * w).sum(axis=1) / total
    else:
        s = rolling.mean(axis=1)

    out = rolling.copy()
    out["S_score"] = s
    out["Recommendation"] = out["S_score"].apply(
        lambda v: "OVERBUY" if v > threshold else "HOLD"
    )
    return out
