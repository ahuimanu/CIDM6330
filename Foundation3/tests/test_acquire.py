import pandas as pd
from pathlib import Path


def fake_get_fred_series(series_id, **kwargs):
    dates = pd.to_datetime(["2020-01-31", "2020-02-29", "2020-03-31"])
    df = pd.DataFrame({"value": [1.0, 2.0, 3.0]}, index=dates)
    df.index.name = "date"
    return df


def test_fetch_all_writes_files(tmp_path, monkeypatch):
    # monkeypatch the helper to avoid network calls
    import Foundation1.FRED_helper as fh

    monkeypatch.setattr(fh, "get_fred_series", fake_get_fred_series)

    from Foundation3.acquire import fetch_all

    series = ["S1", "S2"]
    out = tmp_path / "results"
    frames = fetch_all(series, out)

    # check returned dict
    assert set(frames.keys()) == set(series)

    # check files exist
    for s in series:
        assert (out / f"{s}.csv").exists()

    combined = out / "combined.csv"
    assert combined.exists()

    # combined should have two columns
    df = pd.read_csv(combined, index_col=0, parse_dates=True)
    assert set(df.columns) == set(series)
