from pathlib import Path
from FRED_helper import get_fred_series
import pandas as pd

OUT = Path(__file__).parent / "fred_data"
OUT.mkdir(exist_ok=True)

SERIES = [
    "CPIAUCSL",
    "PCU334111334111",
    "FEDFUNDS",
    "IPG3344S",
    "UMCSENT",
    "DSPIC96",
]

def fetch_all(start_date="2000-01-01", end_date=None):
    frames = {}
    for s in SERIES:
        print("Fetching", s)
        df = get_fred_series(s, start_date=start_date, end_date=end_date)
        if df.empty:
            print("  no data for", s)
            continue
        (OUT / f"{s}.csv").write_text(df.to_csv())
        frames[s] = df["value"].rename(s)
    if not frames:
        print("No series fetched.")
        return
    combined = pd.concat(frames.values(), axis=1)
    combined.to_csv(OUT / "combined.csv")
    print("Saved files to", OUT)

if __name__ == "__main__":
    fetch_all()