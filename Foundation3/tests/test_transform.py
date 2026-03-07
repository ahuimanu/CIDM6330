import pandas as pd
from datetime import datetime


def test_transform_computes_s_score_and_recommendation():
    from Foundation3.transform import transform_combined

    # create raw series that both grow 10% month-over-month
    idx = pd.to_datetime(["2020-01-31", "2020-02-29", "2020-03-31", "2020-04-30"])
    a = [100.0, 110.0, 121.0, 133.1]
    b = [200.0, 220.0, 242.0, 266.2]
    df = pd.DataFrame({"A": a, "B": b}, index=idx)

    out = transform_combined(df, threshold=0.0)

    # after 3-month rolling mean, final row should have 0.10 for each series and S_score 0.10
    # find the last row
    last = out.iloc[-1]
    assert round(last["A"], 6) == round(0.1, 6)
    assert round(last["B"], 6) == round(0.1, 6)
    assert round(last["S_score"], 6) == round(0.1, 6)
    assert last["Recommendation"] == "OVERBUY"
