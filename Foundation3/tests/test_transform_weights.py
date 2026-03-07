import pandas as pd


def test_weighted_s_score():
    from Foundation3.transform import transform_combined

    idx = pd.to_datetime(["2020-01-31", "2020-02-29", "2020-03-31", "2020-04-30"])
    a = [100.0, 110.0, 121.0, 133.1]
    b = [100.0, 100.0, 100.0, 100.0]
    df = pd.DataFrame({"A": a, "B": b}, index=idx)

    # weight A heavily, B zero weight
    weights = {"A": 1.0, "B": 0.0}
    out = transform_combined(df, weights=weights, threshold=0.0)

    last = out.iloc[-1]
    # A percent-change rolling mean should be ~0.10, so S_score should equal A's metric
    assert round(last["S_score"], 6) == round(last["A"], 6)
