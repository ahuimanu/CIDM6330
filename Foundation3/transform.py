import pandas as pd


def transform_combined(
    combined: pd.DataFrame,
    weights: dict[str, float] | None = None,
    threshold: float = 0.0,
    strict: bool = True,
) -> pd.DataFrame:
    """Transform combined raw series into rolling metrics and an `S_score`.

    Steps:
    - compute month-over-month percent change for each series
    - validate that all percent-change values are within [-1.0, 1.0] (Risk 9)
    - compute 3-month rolling mean of percent changes
    - compute `S_score` as weighted average of rolling metrics (equal weights default)
    - add `Recommendation`: 'OVERBUY' when `S_score` < `threshold`, else 'HOLD'

    Args:
        combined: wide DataFrame of raw series (columns=series ids, index=datetime)
        weights: optional mapping of column -> weight (missing keys treated as 0)
        threshold: numeric threshold to decide recommendation
        strict: when True, drop rows where *any* series is NaN instead of *all*
            (Risk 6 — enforces complete-row-only scoring at month boundaries)

    Returns:
        DataFrame containing the rolling metrics, `S_score`, and `Recommendation`.
    """
    if combined is None or combined.empty:
        return pd.DataFrame()

    pct = combined.pct_change()
    dropna_how = "any" if strict else "all"
    pct = pct.dropna(how=dropna_how)

    # Risk 9: validation filter — pct_change() on monthly macro data must produce
    # values in [-1.0, 1.0].  Values outside this range indicate raw (non-normalized)
    # inputs slipped through, which would make the S_score mathematically fraudulent.
    non_null = pct.stack(future_stack=True).dropna()
    if not non_null.empty:
        out_of_range = non_null[(non_null < -1.0) | (non_null > 1.0)]
        if not out_of_range.empty:
            raise ValueError(
                f"Validation filter: {len(out_of_range)} pct_change values outside "
                f"[-1.0, 1.0] — inputs may not be in raw-level form. "
                f"Worst offenders:\n{out_of_range.head()}"
            )

    rolling = pct.rolling(3).mean()
    rolling = rolling.dropna(how=dropna_how)

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
