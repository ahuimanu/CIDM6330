import argparse
import csv
import sqlite3
from collections.abc import Generator, Iterable
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class GdpRow:
    date: str
    value: float


def parse_args() -> argparse.Namespace:
    base = Path(__file__).parent
    parser = argparse.ArgumentParser(
        description="Kata 4: Data transformation pipeline"
    )
    parser.add_argument(
        "--raw-csv",
        default=str(base / "data" / "raw_gdp.csv"),
        help="Path to input CSV file (default: data/raw_gdp.csv)",
    )
    parser.add_argument(
        "--db-path",
        default=str(base / "output" / "gdp.db"),
        help="SQLite database output path (default: output/gdp.db)",
    )
    parser.add_argument(
        "--schema-path",
        default=str(base / "schema.sql"),
        help="Path to schema SQL (default: schema.sql)",
    )
    parser.add_argument(
        "--report-path",
        default=str(base / "report.md"),
        help="Markdown report output path (default: report.md)",
    )
    parser.add_argument(
        "--log-path",
        default=str(base / "output" / "validation.log"),
        help="Validation log output path (default: output/validation.log)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and validate without writing to the database or output files",
    )
    return parser.parse_args()


def extract_rows(csv_path: Path) -> Generator[tuple[int, dict], None, None]:
    """Generator that yields (row_number, row_dict) to support large files."""
    with csv_path.open("r", encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        yield from enumerate(reader, start=2)  # header line is 1


def validate_and_transform(
    rows: Iterable[tuple[int, dict]],
    log_path: Path | None = None,
) -> Generator[GdpRow, None, None]:
    """
    Validates rows; optionally logs malformed records; converts types.
    When log_path is None (dry-run), invalid records are silently counted.
    """
    if log_path is not None:
        log_path.parent.mkdir(parents=True, exist_ok=True)

    def log(msg: str) -> None:
        if log_path is not None:
            with log_path.open("a", encoding="utf-8") as lf:
                lf.write(msg + "\n")

    for line_no, row in rows:
        date = (row.get("date") or "").strip()
        value_raw = (row.get("value") or "").strip()

        if not date:
            log(f"[INVALID] line {line_no}: missing date -> {row}")
            continue

        try:
            value = float(value_raw)
        except ValueError:
            log(f"[INVALID] line {line_no}: invalid value '{value_raw}' -> {row}")
            continue

        yield GdpRow(date=date, value=value)


def init_db(db_path: Path, schema_path: Path) -> None:
    db_path.parent.mkdir(parents=True, exist_ok=True)
    schema_sql = schema_path.read_text(encoding="utf-8")
    with sqlite3.connect(db_path) as conn:
        conn.executescript(schema_sql)
        conn.commit()


def load_rows(db_path: Path, data: Iterable[GdpRow]) -> int:
    """
    Idempotent load: INSERT OR REPLACE by PRIMARY KEY (date).
    Returns number of rows written.
    """
    rows = list(data)
    with sqlite3.connect(db_path) as conn:
        conn.executemany(
            "INSERT OR REPLACE INTO gdp_observations(date, value) VALUES (?, ?)",
            [(r.date, r.value) for r in rows],
        )
        conn.commit()
    return len(rows)


def compute_growth_rates(db_path: Path) -> None:
    """Calculates growth rate compared to previous row and updates table."""
    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT date, value FROM gdp_observations ORDER BY date ASC")
        data = cur.fetchall()

        prev_value: float | None = None
        updates = []
        for date, value in data:
            if prev_value is None:
                growth = None
            else:
                growth = (
                    ((value - prev_value) / prev_value) * 100.0
                    if prev_value != 0
                    else None
                )
            updates.append((growth, date))
            prev_value = value

        cur.executemany(
            "UPDATE gdp_observations SET growth_rate = ? WHERE date = ?", updates
        )
        conn.commit()


def generate_report(db_path: Path, report_path: Path) -> None:
    report_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(db_path) as conn:
        cur = conn.cursor()
        cur.execute("SELECT COUNT(*) FROM gdp_observations")
        count = cur.fetchone()[0]

        cur.execute("SELECT MIN(value), MAX(value), AVG(value) FROM gdp_observations")
        min_v, max_v, avg_v = cur.fetchone()

        cur.execute(
            "SELECT MIN(growth_rate), MAX(growth_rate), AVG(growth_rate) "
            "FROM gdp_observations WHERE growth_rate IS NOT NULL"
        )
        gr = cur.fetchone()
        min_gr, max_gr, avg_gr = gr if gr else (None, None, None)

    md = []
    md.append("# Kata 4 — Data Transformation Pipeline Report\n")
    md.append(f"- Total rows in SQLite: **{count}**\n")
    md.append("## GDP Value Stats\n")
    if count == 0 or min_v is None:
        md.append("- No data available\n")
    else:
        md.append(
            f"- Min: **{min_v:.2f}**\n- Max: **{max_v:.2f}**\n- Avg: **{avg_v:.2f}**\n"
        )
    md.append("\n## Growth Rate Stats\n")
    if min_gr is None:
        md.append("- Not enough data to compute growth rates.\n")
    else:
        md.append(
            f"- Min: **{min_gr:.2f}%**\n"
            f"- Max: **{max_gr:.2f}%**\n"
            f"- Avg: **{avg_gr:.2f}%**\n"
        )

    report_path.write_text("".join(md), encoding="utf-8")


def _dry_run_report(rows: list[GdpRow], db_path: Path) -> None:
    """Print a summary of what the pipeline would do without writing anything."""
    print("[DRY RUN] No files or database will be modified.\n")
    print(f"  Valid rows that WOULD be loaded : {len(rows)}")
    if rows:
        values = [r.value for r in rows]
        print(f"  Date range                      : {rows[0].date} - {rows[-1].date}")
        gdp_range = f"{min(values):.2f} - {max(values):.2f}"
        print(f"  GDP value range                 : {gdp_range}")
    print(f"  Target database                 : {db_path}")


def run_pipeline(
    raw_csv: Path,
    db_path: Path,
    schema_path: Path,
    report_path: Path,
    log_path: Path,
    dry_run: bool = False,
) -> int:
    extracted = extract_rows(raw_csv)

    if dry_run:
        # No log writes, no DB writes, no file writes
        transformed = list(validate_and_transform(extracted, log_path=None))
        _dry_run_report(transformed, db_path)
        return 0

    init_db(db_path, schema_path)
    transformed = validate_and_transform(extracted, log_path=log_path)
    written = load_rows(db_path, transformed)
    compute_growth_rates(db_path)
    generate_report(db_path, report_path)

    print(f"Loaded {written} rows into {db_path}")
    print(f"Wrote report to {report_path}")
    print(f"Validation log at {log_path}")
    return 0


if __name__ == "__main__":
    args = parse_args()
    raise SystemExit(
        run_pipeline(
            raw_csv=Path(args.raw_csv),
            db_path=Path(args.db_path),
            schema_path=Path(args.schema_path),
            report_path=Path(args.report_path),
            log_path=Path(args.log_path),
            dry_run=args.dry_run,
        )
    )
