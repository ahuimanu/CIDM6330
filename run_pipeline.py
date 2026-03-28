from pathlib import Path
import os
import sys
import argparse

# ensure repo root on path
sys.path.insert(0, str(Path(__file__).resolve().parents[0]))


def main(argv=None):
    parser = argparse.ArgumentParser(description="Run the Shortage Scout pipeline (acquire → transform → output)")
    parser.add_argument("--start-date", dest="start_date", help="Start date for acquisition (YYYY-MM-DD)", default=None)
    parser.add_argument("--end-date", dest="end_date", help="End date for acquisition (YYYY-MM-DD)", default=None)
    parser.add_argument("--demo", dest="demo", action="store_true", help="Force demo mode using synthetic data")
    args = parser.parse_args(argv)

    # decide mode based on presence of FRED_API_KEY or --demo flag
    key = os.getenv("FRED_API_KEY")
    if args.demo or not key:
        if not args.demo:
            print("FRED_API_KEY not found — running demo pipeline using synthetic data.")
        from Foundation3.generate_sample import main as demo_main
        demo_main()
        return

    # run real pipeline
    from Foundation3.pipeline import run_pipeline
    SERIES = ["IPG3344S", "CAPUTLG3344SQ", "A34STI", "PCU334413334413"]
    out = Path("Foundation3/results")
    run_pipeline(SERIES, out, start_date=args.start_date, end_date=args.end_date)


if __name__ == "__main__":
    main()
