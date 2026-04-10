import pandas as pd

from Foundation3.transform import transform_combined


def test_transform_declining_supply_triggers_overbuy():
    # declining series — falling supply health should trigger OVERBUY
    idx = pd.to_datetime(["2020-01-31", "2020-02-29", "2020-03-31", "2020-04-30"])
    a = [100.0, 97.0, 94.09, 91.27]  # ~-3% per month
    b = [200.0, 194.0, 188.18, 182.53]
    df = pd.DataFrame({"A": a, "B": b}, index=idx)

    out = transform_combined(df, threshold=0.0)

    last = out.iloc[-1]
    assert last["S_score"] < 0, "Declining supply should produce a negative S_score"
    assert last["Recommendation"] == "OVERBUY"


def test_transform_computes_s_score_and_recommendation():
    # create raw series that both grow 10% month-over-month
    idx = pd.to_datetime(["2020-01-31", "2020-02-29", "2020-03-31", "2020-04-30"])
    a = [100.0, 110.0, 121.0, 133.1]
    b = [200.0, 220.0, 242.0, 266.2]
    df = pd.DataFrame({"A": a, "B": b}, index=idx)

    out = transform_combined(df, threshold=0.0)

    # after 3-month rolling mean, final row should have 0.10 for each series
    last = out.iloc[-1]
    assert round(last["A"], 6) == round(0.1, 6)
    assert round(last["B"], 6) == round(0.1, 6)
    assert round(last["S_score"], 6) == round(0.1, 6)
    # positive S_score (growing supply) → HOLD; shortage signalled by negative score
    assert last["Recommendation"] == "HOLD"
