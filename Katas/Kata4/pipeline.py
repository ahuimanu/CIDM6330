import csv
import sqlite3
import sys
from datetime import datetime

# ============================================================================
# DATA TRANSFORMATION PIPELINE
# ============================================================================
# This pipeline processes raw CSV data through 4 stages:
# 1. EXTRACT - Read raw data from CSV file
# 2. TRANSFORM - Clean, validate, and convert data types
# 3. LOAD - Store transformed data in SQLite database
# 4. REPORT - Query database and generate summary report
# ============================================================================


# STAGE 1: EXTRACT
# Reads rows from CSV file one at a time (generator for memory efficiency)
def extract(csv_file):
    with open(csv_file, "r") as file:
        for row in csv.DictReader(file):
            yield row


# STAGE 2: TRANSFORM
# Validates data quality, removes unwanted columns, converts data types
def transform(raw_data):
    """
    Transform raw data by removing unnecessary columns and validating critical fields.

    Column Selection Rationale:
    - Keep 'date': Essential for time-series analysis (when did this occur?)
    - Keep 'value': The actual data point (what was the interest rate?)
    - Drop 'realtime_start' and 'realtime_end': Metadata about FRED's record updates,
      not relevant to analyzing the actual interest rate movements. This reduces
      storage and improves query performance without losing important information.

    Validation:
    - Reject any rows with empty 'date' or 'value' fields (malformed records)
    - Convert date from text to datetime object
    - Convert value from text to float (decimal number)
    """
    for row in raw_data:
        if not row["date"]:  # if date is empty (blank)
            continue  # skip this row
        if not row["value"]:  # if value is empty (blank)
            continue  # skip this row
        yield {
            "date": datetime.strptime(row["date"], "%Y-%m-%d"),
            "value": float(row["value"]),
        }


# STAGE 3: LOAD
# Writes transformed data into SQLite database table
# Uses INSERT OR REPLACE to handle duplicates (idempotent)
def load(db_file, transformed_data):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Create table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS interest_rates (
            date TEXT PRIMARY KEY,
            value REAL
        )
    """)

    # Insert transformed data into the database
    for record in transformed_data:
        cursor.execute(
            """
            INSERT OR REPLACE INTO interest_rates (date, value) VALUES (?, ?)
        """,
            (record["date"].strftime("%Y-%m-%d"), record["value"]),
        )

    conn.commit()
    conn.close()


# STAGE 4: REPORT
# Queries the SQLite database to generate summary statistics
# Writes results to markdown file for human-readable output
def report(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Query to get the average interest rate
    cursor.execute("SELECT AVG(value) FROM interest_rates")
    average_rate = cursor.fetchone()[0]
    cursor.execute("SELECT COUNT(*) FROM interest_rates")
    total_records = cursor.fetchone()[0]
    cursor.execute("SELECT MIN(date), MAX(date) FROM interest_rates")
    date_range = cursor.fetchone()  # (min_date, max_date)
    cursor.execute("SELECT MAX(value) FROM interest_rates")
    max_rate = cursor.fetchone()[0]

    # Unpack the date range
    min_date, max_date = date_range

    # Write to markdown file
    with open("report.md", "w") as f:
        f.write("# Federal Funds Rate Report\n\n")
        f.write("## Statistics\n\n")
        f.write(f"- **Total Records**: {total_records}\n")
        f.write(f"- **Date Range**: {min_date} to {max_date}\n")
        f.write(f"- **Maximum Rate**: {max_rate:.2f}%\n")
        f.write(f"- **Average Rate**: {average_rate:.2f}%\n")

    conn.close()


def preview(transformed_data, num_rows=5):
    """Show a preview of transformed data without writing to database"""
    rows_seen = 0
    print(f"\n=== DRY-RUN: Preview of first {num_rows} transformed records ===\n")
    for row in transformed_data:
        if rows_seen >= num_rows:
            break
        print(f"  Date: {row['date'].isoformat()}, Rate: {row['value']:.2f}%")
        rows_seen += 1
    print(f"\n(Use without --dry-run to actually load to database)\n")


def main(csv_file, db_file, dry_run=False):
    raw_data = extract(csv_file)
    transformed_data = transform(raw_data)

    if dry_run:
        preview(transformed_data)
    else:
        load(db_file, transformed_data)
        report(db_file)


if __name__ == "__main__":
    csv_file = r"C:\Users\patry\OneDrive\Documents\GitHub\CIDM6330-Spring2026-Patrick-Perez\CIDM6330\Foundation1\fred_data\FEDFUNDS.csv"
    db_file = "fed_rates.db"
    dry_run = "--dry-run" in sys.argv
    main(csv_file, db_file, dry_run=dry_run)
