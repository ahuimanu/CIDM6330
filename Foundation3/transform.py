import pandas as pd


def transform_combined(
    combined: pd.DataFrame,
    weights: dict[str, float] | None = None,
    threshold: float = 0.0,
) -> pd.DataFrame:
    """Transform combined raw series into rolling metrics and an `S_score`.

    Steps:
    - compute month-over-month percent change for each series
    - compute 3-month rolling mean of percent changes
    - compute `S_score` as weighted average of rolling metrics (equal weights default)
    - add `Recommendation`: 'OVERBUY' when `S_score` < `threshold`, else 'HOLD'

    Args:
        combined: wide DataFrame of raw series (columns=series ids, index=datetime)
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
        s = rolling.mean(axis=1) if total == 0 else (rolling * w).sum(axis=1) / total
    else:
        s = rolling.mean(axis=1)

    out = rolling.copy()
    out["S_score"] = s
    # OVERBUY when S_score falls below threshold — a declining supply health score
    # (negative rolling average) signals a contraction that warrants stockpiling.
    out["Recommendation"] = out["S_score"].apply(
        lambda v: "OVERBUY" if v < threshold else "HOLD"
    )
    return out
