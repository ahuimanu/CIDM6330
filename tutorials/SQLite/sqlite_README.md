# Database Operations with SQLite

SQLite is a self-contained, serverless SQL database engine included in Python's standard library. It's ideal for learning SQL concepts, prototyping, embedded applications, and single-user scenarios. This guide covers SQLite fundamentals and introduces the Repository pattern for clean data access.

## Table of Contents

1. [SQLite Overview](#sqlite-overview)
2. [Connecting to Databases](#connecting-to-databases)
3. [Creating Tables](#creating-tables)
4. [CRUD Operations](#crud-operations)
5. [Parameterized Queries](#parameterized-queries)
6. [Transactions](#transactions)
7. [Working with Results](#working-with-results)
8. [The Repository Pattern](#the-repository-pattern)
9. [Advanced Patterns](#advanced-patterns)
10. [Best Practices](#best-practices)

---

## SQLite Overview

### Why SQLite?

- **Zero configuration**: No server to install or manage
- **Self-contained**: Single file contains the entire database
- **Cross-platform**: Database files work on any OS
- **Reliable**: ACID-compliant with full transaction support
- **Included**: Part of Python's standard library (`sqlite3`)

### When to Use SQLite

| Use Case | SQLite | PostgreSQL/MySQL |
|----------|--------|------------------|
| Embedded/mobile apps | ✓ | |
| Prototyping | ✓ | |
| Single-user apps | ✓ | |
| Testing | ✓ | |
| Small-medium websites | ✓ | ✓ |
| High concurrency | | ✓ |
| Multi-user apps | | ✓ |
| Large scale | | ✓ |

---

## Connecting to Databases

### Basic Connection

```python
import sqlite3

# Connect to file-based database (creates if doesn't exist)
conn = sqlite3.connect("airports.db")

# Connect to in-memory database (temporary, for testing)
conn = sqlite3.connect(":memory:")

# Always close when done
conn.close()
```

### Using Context Managers

```python
import sqlite3

# Connection as context manager (auto-commits on success, rolls back on exception)
with sqlite3.connect("airports.db") as conn:
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM airports")
    # Auto-commits if no exception
# Note: Connection is NOT automatically closed, just committed

# Full cleanup pattern
def get_connection(db_path: str) -> sqlite3.Connection:
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row  # Enable dict-like row access
    return conn

# Best practice: explicit connection management
conn = get_connection("airports.db")
try:
    # Work with database
    pass
finally:
    conn.close()
```

### Connection Options

```python
import sqlite3

conn = sqlite3.connect(
    "airports.db",
    timeout=30.0,              # Wait up to 30s for locks
    detect_types=sqlite3.PARSE_DECLTYPES,  # Auto-convert types
    isolation_level="DEFERRED",  # Transaction isolation
)

# Enable foreign key enforcement (off by default!)
conn.execute("PRAGMA foreign_keys = ON")

# Enable WAL mode for better concurrency
conn.execute("PRAGMA journal_mode = WAL")
```

---

## Creating Tables

### Basic Table Creation

```python
import sqlite3

conn = sqlite3.connect("airports.db")
cursor = conn.cursor()

# Create table with various column types
cursor.execute("""
    CREATE TABLE IF NOT EXISTS airports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        stationid TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        city TEXT,
        state TEXT,
        latitude REAL,
        longitude REAL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
""")

conn.commit()
```

### SQLite Data Types

SQLite uses dynamic typing with five storage classes:

| Storage Class | Python Type | Description |
|---------------|-------------|-------------|
| NULL | None | Null value |
| INTEGER | int | Signed integer |
| REAL | float | Floating point |
| TEXT | str | Text string |
| BLOB | bytes | Binary data |

### Tables with Foreign Keys

```python
cursor.execute("""
    CREATE TABLE IF NOT EXISTS runways (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        airport_id INTEGER NOT NULL,
        identifier TEXT NOT NULL,
        length_ft INTEGER NOT NULL,
        width_ft INTEGER,
        surface TEXT,
        FOREIGN KEY (airport_id) REFERENCES airports(id)
            ON DELETE CASCADE
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS weather_reports (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        airport_id INTEGER NOT NULL,
        metar TEXT,
        taf TEXT,
        fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (airport_id) REFERENCES airports(id)
            ON DELETE CASCADE
    )
""")

conn.commit()
```

### Indexes

```python
# Create index for frequently queried columns
cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_airports_stationid 
    ON airports(stationid)
""")

cursor.execute("""
    CREATE INDEX IF NOT EXISTS idx_runways_airport_id 
    ON runways(airport_id)
""")

conn.commit()
```

---

## CRUD Operations

### Create (INSERT)

```python
# Insert single row
cursor.execute("""
    INSERT INTO airports (stationid, name, city, state, latitude, longitude)
    VALUES (?, ?, ?, ?, ?, ?)
""", ("KAMA", "Rick Husband Amarillo International Airport", "Amarillo", "TX", 35.2194, -101.7059))

# Get the auto-generated ID
airport_id = cursor.lastrowid
print(f"Inserted airport with ID: {airport_id}")

# Insert multiple rows
airports_data = [
    ("KLBB", "Lubbock Preston Smith International", "Lubbock", "TX", 33.6636, -101.8228),
    ("KMAF", "Midland International Air and Space Port", "Midland", "TX", 31.9425, -102.2019),
]
cursor.executemany("""
    INSERT INTO airports (stationid, name, city, state, latitude, longitude)
    VALUES (?, ?, ?, ?, ?, ?)
""", airports_data)

conn.commit()
```

### Read (SELECT)

```python
# Select all
cursor.execute("SELECT * FROM airports")
all_airports = cursor.fetchall()

# Select with condition
cursor.execute("SELECT * FROM airports WHERE state = ?", ("TX",))
texas_airports = cursor.fetchall()

# Select one
cursor.execute("SELECT * FROM airports WHERE stationid = ?", ("KAMA",))
airport = cursor.fetchone()

# Select specific columns
cursor.execute("SELECT stationid, name FROM airports ORDER BY name")
for row in cursor.fetchall():
    print(f"{row[0]}: {row[1]}")

# Select with JOIN
cursor.execute("""
    SELECT a.stationid, a.name, r.identifier, r.length_ft
    FROM airports a
    LEFT JOIN runways r ON a.id = r.airport_id
    ORDER BY a.stationid
""")
```

### Update

```python
# Update single row
cursor.execute("""
    UPDATE airports 
    SET name = ?, city = ?
    WHERE stationid = ?
""", ("Amarillo International Airport", "Amarillo", "KAMA"))

# Check rows affected
print(f"Updated {cursor.rowcount} rows")

# Update with condition
cursor.execute("""
    UPDATE airports 
    SET state = 'Texas'
    WHERE state = 'TX'
""")

conn.commit()
```

### Delete

```python
# Delete single row
cursor.execute("DELETE FROM airports WHERE stationid = ?", ("KXYZ",))

# Delete with condition
cursor.execute("DELETE FROM weather_reports WHERE fetched_at < date('now', '-7 days')")

# Check rows affected
print(f"Deleted {cursor.rowcount} rows")

conn.commit()
```

---

## Parameterized Queries

**ALWAYS use parameterized queries to prevent SQL injection attacks.**

### Why Parameterization Matters

```python
# DANGEROUS - SQL Injection vulnerability!
stationid = "KAMA'; DROP TABLE airports; --"
cursor.execute(f"SELECT * FROM airports WHERE stationid = '{stationid}'")

# SAFE - Parameterized query
stationid = "KAMA'; DROP TABLE airports; --"
cursor.execute("SELECT * FROM airports WHERE stationid = ?", (stationid,))
# The malicious input is treated as a literal string, not SQL code
```

### Positional Parameters (?)

```python
# Single parameter (note the comma to make it a tuple)
cursor.execute("SELECT * FROM airports WHERE stationid = ?", ("KAMA",))

# Multiple parameters
cursor.execute("""
    SELECT * FROM airports 
    WHERE state = ? AND latitude > ?
""", ("TX", 33.0))
```

### Named Parameters (:name)

```python
# Named parameters - more readable for many parameters
cursor.execute("""
    INSERT INTO airports (stationid, name, city, state, latitude, longitude)
    VALUES (:stationid, :name, :city, :state, :lat, :lon)
""", {
    "stationid": "KDFW",
    "name": "Dallas/Fort Worth International",
    "city": "Dallas",
    "state": "TX",
    "lat": 32.8998,
    "lon": -97.0403,
})

# Named parameters with SELECT
cursor.execute("""
    SELECT * FROM airports 
    WHERE state = :state AND latitude BETWEEN :min_lat AND :max_lat
""", {"state": "TX", "min_lat": 30.0, "max_lat": 35.0})
```

---

## Transactions

SQLite supports ACID transactions. By default, `sqlite3` operates in auto-commit mode unless you start a transaction.

### Explicit Transactions

```python
conn = sqlite3.connect("airports.db")
conn.execute("PRAGMA foreign_keys = ON")

try:
    cursor = conn.cursor()
    
    # Start transaction (implicit with first statement)
    cursor.execute("""
        INSERT INTO airports (stationid, name, city, state)
        VALUES (?, ?, ?, ?)
    """, ("KHOU", "William P. Hobby Airport", "Houston", "TX"))
    
    airport_id = cursor.lastrowid
    
    cursor.execute("""
        INSERT INTO runways (airport_id, identifier, length_ft, surface)
        VALUES (?, ?, ?, ?)
    """, (airport_id, "12R/30L", 7602, "concrete"))
    
    # Commit transaction
    conn.commit()
    print("Transaction committed successfully")
    
except sqlite3.Error as e:
    # Rollback on error
    conn.rollback()
    print(f"Transaction rolled back: {e}")
    
finally:
    conn.close()
```

### Context Manager Transactions

```python
# The connection context manager handles commit/rollback
with sqlite3.connect("airports.db") as conn:
    cursor = conn.cursor()
    cursor.execute("INSERT INTO airports (stationid, name) VALUES (?, ?)", 
                   ("KSAT", "San Antonio International"))
    # Commits automatically if no exception
# Rolls back automatically if exception occurs
```

### Savepoints (Nested Transactions)

```python
conn = sqlite3.connect("airports.db")
cursor = conn.cursor()

try:
    # Outer transaction
    cursor.execute("INSERT INTO airports (stationid, name) VALUES (?, ?)",
                   ("KAUS", "Austin-Bergstrom International"))
    
    # Create savepoint
    cursor.execute("SAVEPOINT add_runways")
    
    try:
        cursor.execute("INSERT INTO runways (airport_id, identifier, length_ft) VALUES (?, ?, ?)",
                       (cursor.lastrowid, "17L/35R", 12250))
        # Intentional error for demo
        cursor.execute("INSERT INTO runways (airport_id, identifier, length_ft) VALUES (?, ?, ?)",
                       (9999, "BAD", 0))  # Invalid airport_id
    except sqlite3.Error:
        # Rollback to savepoint (keeps outer transaction)
        cursor.execute("ROLLBACK TO SAVEPOINT add_runways")
        print("Runway insert failed, rolled back to savepoint")
    
    cursor.execute("RELEASE SAVEPOINT add_runways")
    conn.commit()
    
finally:
    conn.close()
```

---

## Working with Results

### Row Factory

By default, rows are returned as tuples. Use `Row` for dict-like access.

```python
import sqlite3

conn = sqlite3.connect("airports.db")
conn.row_factory = sqlite3.Row  # Enable Row factory

cursor = conn.cursor()
cursor.execute("SELECT * FROM airports WHERE stationid = ?", ("KAMA",))
row = cursor.fetchone()

if row:
    # Access by column name
    print(row["stationid"])
    print(row["name"])
    
    # Access by index still works
    print(row[0])
    
    # Get column names
    print(row.keys())
    
    # Convert to dict
    airport_dict = dict(row)
```

### Custom Row Factory

```python
from dataclasses import dataclass

@dataclass
class Airport:
    id: int
    stationid: str
    name: str
    city: str
    state: str

def airport_factory(cursor, row):
    """Convert row to Airport dataclass."""
    columns = [column[0] for column in cursor.description]
    data = dict(zip(columns, row))
    return Airport(
        id=data["id"],
        stationid=data["stationid"],
        name=data["name"],
        city=data.get("city", ""),
        state=data.get("state", ""),
    )

conn = sqlite3.connect("airports.db")
conn.row_factory = airport_factory

cursor = conn.cursor()
cursor.execute("SELECT id, stationid, name, city, state FROM airports")

for airport in cursor.fetchall():
    print(f"{airport.stationid}: {airport.name}")  # It's now an Airport object!
```

### Iterating Over Results

```python
# Fetch all into memory (fine for small result sets)
cursor.execute("SELECT * FROM airports")
airports = cursor.fetchall()

# Iterate without loading all into memory (better for large results)
cursor.execute("SELECT * FROM airports")
for row in cursor:
    print(row)

# Fetch in batches
cursor.execute("SELECT * FROM airports")
while True:
    batch = cursor.fetchmany(100)
    if not batch:
        break
    for row in batch:
        process(row)
```

---

## The Repository Pattern

The Repository pattern abstracts data access, separating domain logic from database operations. This makes code more testable and maintainable.

### Basic Repository

```python
import sqlite3
from dataclasses import dataclass
from typing import Protocol
from abc import ABC, abstractmethod

@dataclass
class Airport:
    id: int | None
    stationid: str
    name: str
    city: str
    state: str

class AirportRepository(ABC):
    """Abstract repository defining the interface."""
    
    @abstractmethod
    def get_by_id(self, id: int) -> Airport | None:
        pass
    
    @abstractmethod
    def get_by_stationid(self, stationid: str) -> Airport | None:
        pass
    
    @abstractmethod
    def get_all(self) -> list[Airport]:
        pass
    
    @abstractmethod
    def save(self, airport: Airport) -> Airport:
        pass
    
    @abstractmethod
    def delete(self, id: int) -> bool:
        pass


class SQLiteAirportRepository(AirportRepository):
    """SQLite implementation of the airport repository."""
    
    def __init__(self, connection: sqlite3.Connection):
        self._conn = connection
        self._conn.row_factory = sqlite3.Row
    
    def get_by_id(self, id: int) -> Airport | None:
        cursor = self._conn.execute(
            "SELECT * FROM airports WHERE id = ?", (id,)
        )
        row = cursor.fetchone()
        return self._row_to_airport(row) if row else None
    
    def get_by_stationid(self, stationid: str) -> Airport | None:
        cursor = self._conn.execute(
            "SELECT * FROM airports WHERE stationid = ?", (stationid,)
        )
        row = cursor.fetchone()
        return self._row_to_airport(row) if row else None
    
    def get_all(self) -> list[Airport]:
        cursor = self._conn.execute("SELECT * FROM airports ORDER BY stationid")
        return [self._row_to_airport(row) for row in cursor.fetchall()]
    
    def save(self, airport: Airport) -> Airport:
        if airport.id is None:
            # Insert new
            cursor = self._conn.execute("""
                INSERT INTO airports (stationid, name, city, state)
                VALUES (?, ?, ?, ?)
            """, (airport.stationid, airport.name, airport.city, airport.state))
            airport.id = cursor.lastrowid
        else:
            # Update existing
            self._conn.execute("""
                UPDATE airports 
                SET stationid = ?, name = ?, city = ?, state = ?
                WHERE id = ?
            """, (airport.stationid, airport.name, airport.city, airport.state, airport.id))
        
        self._conn.commit()
        return airport
    
    def delete(self, id: int) -> bool:
        cursor = self._conn.execute("DELETE FROM airports WHERE id = ?", (id,))
        self._conn.commit()
        return cursor.rowcount > 0
    
    def _row_to_airport(self, row: sqlite3.Row) -> Airport:
        return Airport(
            id=row["id"],
            stationid=row["stationid"],
            name=row["name"],
            city=row["city"] or "",
            state=row["state"] or "",
        )
```

### Using the Repository

```python
# Production code
conn = sqlite3.connect("airports.db")
repo = SQLiteAirportRepository(conn)

# Create
new_airport = Airport(None, "KIAH", "George Bush Intercontinental", "Houston", "TX")
saved = repo.save(new_airport)
print(f"Created airport with ID: {saved.id}")

# Read
airport = repo.get_by_stationid("KAMA")
if airport:
    print(f"Found: {airport.name}")

# Update
airport.name = "Updated Name"
repo.save(airport)

# Delete
repo.delete(airport.id)

# List all
for airport in repo.get_all():
    print(f"{airport.stationid}: {airport.name}")
```

### In-Memory Repository for Testing

```python
class InMemoryAirportRepository(AirportRepository):
    """In-memory implementation for testing."""
    
    def __init__(self):
        self._airports: dict[int, Airport] = {}
        self._next_id = 1
    
    def get_by_id(self, id: int) -> Airport | None:
        return self._airports.get(id)
    
    def get_by_stationid(self, stationid: str) -> Airport | None:
        for airport in self._airports.values():
            if airport.stationid == stationid:
                return airport
        return None
    
    def get_all(self) -> list[Airport]:
        return sorted(self._airports.values(), key=lambda a: a.stationid)
    
    def save(self, airport: Airport) -> Airport:
        if airport.id is None:
            airport.id = self._next_id
            self._next_id += 1
        self._airports[airport.id] = airport
        return airport
    
    def delete(self, id: int) -> bool:
        if id in self._airports:
            del self._airports[id]
            return True
        return False

# Now tests can use InMemoryAirportRepository
# Production uses SQLiteAirportRepository
# Same interface, swappable implementations
```

---

## Advanced Patterns

### Unit of Work

Coordinate multiple repository operations in a single transaction.

```python
class UnitOfWork:
    """Manages transactions across multiple repositories."""
    
    def __init__(self, db_path: str):
        self._db_path = db_path
        self._conn: sqlite3.Connection | None = None
    
    def __enter__(self):
        self._conn = sqlite3.connect(self._db_path)
        self._conn.execute("PRAGMA foreign_keys = ON")
        self.airports = SQLiteAirportRepository(self._conn)
        self.runways = SQLiteRunwayRepository(self._conn)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None:
            self._conn.commit()
        else:
            self._conn.rollback()
        self._conn.close()
        return False

# Usage
with UnitOfWork("airports.db") as uow:
    airport = Airport(None, "KDEN", "Denver International", "Denver", "CO")
    saved_airport = uow.airports.save(airport)
    
    runway = Runway(None, saved_airport.id, "16R/34L", 16000, "concrete")
    uow.runways.save(runway)
    
    # Both operations commit together or roll back together
```

### Query Builder Pattern

For complex dynamic queries.

```python
class AirportQuery:
    """Build complex queries fluently."""
    
    def __init__(self):
        self._conditions: list[str] = []
        self._params: list = []
        self._order_by: str | None = None
        self._limit: int | None = None
    
    def in_state(self, state: str) -> "AirportQuery":
        self._conditions.append("state = ?")
        self._params.append(state)
        return self
    
    def name_contains(self, text: str) -> "AirportQuery":
        self._conditions.append("name LIKE ?")
        self._params.append(f"%{text}%")
        return self
    
    def with_min_runway(self, length_ft: int) -> "AirportQuery":
        self._conditions.append("""
            id IN (SELECT airport_id FROM runways WHERE length_ft >= ?)
        """)
        self._params.append(length_ft)
        return self
    
    def order_by(self, column: str) -> "AirportQuery":
        self._order_by = column
        return self
    
    def limit(self, n: int) -> "AirportQuery":
        self._limit = n
        return self
    
    def build(self) -> tuple[str, list]:
        sql = "SELECT * FROM airports"
        
        if self._conditions:
            sql += " WHERE " + " AND ".join(self._conditions)
        
        if self._order_by:
            sql += f" ORDER BY {self._order_by}"
        
        if self._limit:
            sql += f" LIMIT {self._limit}"
        
        return sql, self._params

# Usage
query = (
    AirportQuery()
    .in_state("TX")
    .with_min_runway(10000)
    .order_by("name")
    .limit(10)
)

sql, params = query.build()
cursor.execute(sql, params)
```

---

## Best Practices

### 1. Always Use Parameterized Queries

```python
# NEVER do this
cursor.execute(f"SELECT * FROM airports WHERE stationid = '{user_input}'")

# ALWAYS do this
cursor.execute("SELECT * FROM airports WHERE stationid = ?", (user_input,))
```

### 2. Enable Foreign Keys

```python
# Foreign keys are disabled by default in SQLite!
conn = sqlite3.connect("airports.db")
conn.execute("PRAGMA foreign_keys = ON")
```

### 3. Use Connection Context Managers

```python
with sqlite3.connect("airports.db") as conn:
    # Auto-commits on success, rolls back on exception
    pass
```

### 4. Set Row Factory for Readable Code

```python
conn.row_factory = sqlite3.Row
# Now use row["column_name"] instead of row[0]
```

### 5. Handle NULL Values

```python
# SQLite NULL becomes Python None
cursor.execute("SELECT city FROM airports WHERE stationid = ?", ("KAMA",))
row = cursor.fetchone()
city = row[0] if row and row[0] else "Unknown"

# Or with row factory
city = row["city"] or "Unknown"
```

### 6. Use Transactions for Related Operations

```python
try:
    cursor.execute("INSERT INTO airports ...")
    airport_id = cursor.lastrowid
    cursor.execute("INSERT INTO runways ... VALUES (?, ...)", (airport_id,))
    conn.commit()
except sqlite3.Error:
    conn.rollback()
    raise
```

### 7. Index Frequently Queried Columns

```python
# Speeds up WHERE and JOIN on these columns
cursor.execute("CREATE INDEX IF NOT EXISTS idx_stationid ON airports(stationid)")
```

### 8. Use Migrations for Schema Changes

```python
def migrate(conn: sqlite3.Connection) -> None:
    """Apply database migrations."""
    cursor = conn.cursor()
    
    # Check current version
    cursor.execute("PRAGMA user_version")
    version = cursor.fetchone()[0]
    
    if version < 1:
        cursor.execute("""
            CREATE TABLE airports (
                id INTEGER PRIMARY KEY,
                stationid TEXT UNIQUE NOT NULL,
                name TEXT NOT NULL
            )
        """)
        cursor.execute("PRAGMA user_version = 1")
    
    if version < 2:
        cursor.execute("ALTER TABLE airports ADD COLUMN city TEXT")
        cursor.execute("ALTER TABLE airports ADD COLUMN state TEXT")
        cursor.execute("PRAGMA user_version = 2")
    
    conn.commit()
```

---

## Further Reading

- [sqlite3 documentation](https://docs.python.org/3/library/sqlite3.html)
- [SQLite documentation](https://www.sqlite.org/docs.html)
- [Repository Pattern](https://martinfowler.com/eaaCatalog/repository.html) - Martin Fowler
- [Unit of Work Pattern](https://martinfowler.com/eaaCatalog/unitOfWork.html) - Martin Fowler
