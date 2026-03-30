from pathlib import Path
import sys
import json
from typing import Tuple, Dict

# Ensure local package imports work when running from repo root
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from FRED_helper import get_fred_series
import pandas as pd

OUT = HERE / "fred_data"
OUT.mkdir(exist_ok=True)


def compute_lag_correlation(
    lead_series: str,
    target_series: str,
    start_date: str = "2000-01-01",
    max_lag: int = 12,
) -> Tuple[Dict[int, float], int, float]:
    a = get_fred_series(lead_series, start_date=start_date)
    b = get_fred_series(target_series, start_date=start_date)
    if a.empty or b.empty:
        raise RuntimeError(
            "One of the series returned no data; check your FRED API key and network"
        )
    sa = a["value"].rename(lead_series)
    sb = b["value"].rename(target_series)
    df = pd.concat([sa, sb], axis=1).dropna()
    results = {}
    for lag in range(0, max_lag + 1):
        # lag = months that lead_series leads target_series
        corr = df[lead_series].corr(df[target_series].shift(-lag))
        results[lag] = None if pd.isna(corr) else float(corr)
    series = pd.Series(results)
    best = int(series.abs().idxmax())
    best_corr = series[best]
    return results, best, best_corr


if __name__ == "__main__":
    lead = "IPG3344S"
    target = "CPIAUCSL"
    print(f"Computing lag correlations: does `{lead}` lead `{target}`?")
    res, best, corr = compute_lag_correlation(lead, target)
    print(f"Best lag (months) where {lead} leads {target}: {best} (corr={corr:.4f})")
    (OUT / "lag_results.json").write_text(json.dumps(res, indent=2))
    print("Wrote:", OUT / "lag_results.json")
