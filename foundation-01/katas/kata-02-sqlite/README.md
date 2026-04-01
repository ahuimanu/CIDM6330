\# Kata 2 — Data Persistence (SQLite)



\## What it does

\- Creates a SQLite DB with two related tables: stations and observations

\- Implements CRUD functions using parameterized queries

\- Includes a join query for meaningful results

\- Includes a seed() function to populate sample data



\## Quick test (from this folder)

py -c "from kata2.weather\_db import connect, create\_schema, seed, get\_station\_daily\_summary; from pathlib import Path; db=Path('weather.db'); conn=connect(db); create\_schema(conn); seed(conn); print(get\_station\_daily\_summary(conn,'2026-02-01','2026-02-03',10.0))"



