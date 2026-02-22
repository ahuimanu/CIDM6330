# Kata 02  SQLite Operations (Beginner)

This kata demonstrates basic SQLite operations in Python. The implementation
has been refactored to match the tutorials example: richer schema, domain
models, repository pattern, UnitOfWork, and a comprehensive demo.

Quick steps

1. Create a feature branch:

   git checkout -b kata-02-sqlite

2. Implement and test in [Kata2/sqlite_kata.py](Kata2/sqlite_kata.py#L1).

3. Seed and inspect the database using the module's demo or the `sqlite3` CLI.

4. Merge back to main and delete the branch:

   git checkout main
   git merge kata-02-sqlite
   git branch -d kata-02-sqlite

What changed

- The module now exposes `Airport`, `Runway`, and `WeatherReport` dataclasses.
- Schema is centralized in `SCHEMA` and created via `init_database(conn)`.
- A `SQLiteAirportRepository` encapsulates CRUD and related joins.
- A `UnitOfWork` context manager controls connections and transactions.
- An in-memory repository and pytest tests are provided for quick testing.

Primary API and usage

Use the `UnitOfWork` for simple scripted usage (demo shown in the module):

```python
from Kata2 import sqlite_kata

with sqlite_kata.UnitOfWork("kata2_demo.db") as uow:
    sqlite_kata.seed_database(uow._conn)
    rows = uow.airports.flights_with_airports() if uow.airports else []
    for r in rows:
        print(dict(r))
```

Programmatic example

```python
from Kata2.sqlite_kata import SQLiteAirportRepository, connect_db, init_database, Airport

conn = connect_db(":memory:")
init_database(conn)
repo = SQLiteAirportRepository(conn)
airport = Airport(None, "LAX", "Los Angeles Intl", "Los Angeles", "CA")
saved = repo.save(airport)
```

Testing

- Run the provided tests with: pytest Kata2/test_sqlite_kata.py

How to run the demo

Run the demo in the module directly:

python Kata2/sqlite_kata.py

Or run the example usage script:

python -m Kata2.example_usage

Notes

- Use `UnitOfWork` or explicit `conn.commit()` to control transaction boundaries.
- See [Kata2/sqlite_kata.py](Kata2/sqlite_kata.py#L1) for full examples and
  additional helper classes.
