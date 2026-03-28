from Katas.Kata4 import pipeline
from datetime import datetime
from pathlib import Path


def main():
    out_dir = Path(__file__).parent
    db_file = out_dir / "sample.db"

    # sample transformed records
    transformed = [
        {"date": datetime(2020, 1, 1), "value": 1.2},
        {"date": datetime(2020, 1, 2), "value": 2.4},
    ]

    # write DB
    pipeline.load(str(db_file), transformed)

    # generate report.md in current working directory and move into out_dir
    pipeline.report(str(db_file))
    report_src = Path("report.md")
    if report_src.exists():
        report_src.rename(out_dir / "report.md")
        print(f"Wrote {out_dir / 'report.md'}")
    else:
        print("report.md not created")


if __name__ == '__main__':
    main()
