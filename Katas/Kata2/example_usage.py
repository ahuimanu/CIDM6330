"""Example usage for Kata2.sqlite_kata using the new repository API."""
from pathlib import Path
from Kata2 import sqlite_kata


def demo(db_path: str = "Kata2/output/kata2_demo.db"):
    """Create DB, seed it, show explain plan before/after index, and return rows.

    Returns a tuple: (plan_before, plan_after, joined_rows)
    """
    # Ensure directory exists
    p = Path(db_path)
    if p.parent and not p.parent.exists():
        p.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite_kata.connect_db(db_path)
    sqlite_kata.init_database(conn)
    # seed_database is idempotent
    sqlite_kata.seed_database(conn)

    repo = sqlite_kata.SQLiteAirportRepository(conn)

    # Demonstrate explain plan before/after recreating the index
    conn.execute("DROP INDEX IF EXISTS idx_flights_src")
    before = repo.explain_query_plan("SELECT * FROM flights WHERE src_airport_id = ?", (1,))

    conn.execute("CREATE INDEX IF NOT EXISTS idx_flights_src ON flights(src_airport_id)")
    after = repo.explain_query_plan("SELECT * FROM flights WHERE src_airport_id = ?", (1,))

    rows = repo.flights_with_airports()
    conn.close()
    return before, after, rows


if __name__ == "__main__":
    before, after, rows = demo()
    print("EXPLAIN before:")
    for r in before:
        print(dict(r))
    print("\nEXPLAIN after:")
    for r in after:
        print(dict(r))
    print("\nFlights joined:")
    for r in rows:
        print(dict(r))
