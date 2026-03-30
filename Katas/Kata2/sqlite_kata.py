"""
sqlite_kata

A kata module implementing a richer SQLite demo adapted from the tutorials
example. This file intentionally mirrors the tutorial's structure so its
printed demonstration output matches the example.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field
from datetime import datetime
from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Optional

# =============================================================================
# DOMAIN MODELS
# =============================================================================


@dataclass
class Runway:
    id: int | None
    airport_id: int
    identifier: str
    length_ft: int
    width_ft: int
    surface: str


@dataclass
class WeatherReport:
    id: int | None
    airport_id: int
    metar: str | None
    taf: str | None
    fetched_at: datetime = field(default_factory=datetime.now)


@dataclass
class Airport:
    id: int | None
    stationid: str
    name: str
    city: str
    state: str
    latitude: float | None = None
    longitude: float | None = None
    runways: list[Runway] = field(default_factory=list)
    weather: WeatherReport | None = None


# =============================================================================
# DATABASE SCHEMA
# =============================================================================

SCHEMA = """
CREATE TABLE IF NOT EXISTS airports (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	stationid TEXT NOT NULL UNIQUE,
	name TEXT NOT NULL,
	city TEXT,
	state TEXT,
	latitude REAL,
	longitude REAL,
	created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS runways (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	airport_id INTEGER NOT NULL,
	identifier TEXT NOT NULL,
	length_ft INTEGER NOT NULL,
	width_ft INTEGER,
	surface TEXT,
	FOREIGN KEY (airport_id) REFERENCES airports(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS weather_reports (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	airport_id INTEGER NOT NULL,
	metar TEXT,
	taf TEXT,
	fetched_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY (airport_id) REFERENCES airports(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_airports_stationid ON airports(stationid);
CREATE INDEX IF NOT EXISTS idx_runways_airport_id ON runways(airport_id);
CREATE INDEX IF NOT EXISTS idx_weather_airport_id ON weather_reports(airport_id);
"""


def init_database(conn: sqlite3.Connection) -> None:
    conn.executescript(SCHEMA)
    conn.commit()


# =============================================================================
# REPOSITORY PATTERN
# =============================================================================


class AirportRepository(ABC):
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
    def get_by_state(self, state: str) -> list[Airport]:
        pass

    @abstractmethod
    def save(self, airport: Airport) -> Airport:
        pass

    @abstractmethod
    def delete(self, id: int) -> bool:
        pass


class SQLiteAirportRepository(AirportRepository):
    def __init__(self, connection: sqlite3.Connection):
        self._conn = connection
        self._conn.row_factory = sqlite3.Row

    def get_by_id(self, id: int) -> Airport | None:
        cursor = self._conn.execute("SELECT * FROM airports WHERE id = ?", (id,))
        row = cursor.fetchone()
        return self._row_to_airport(row, include_relations=True) if row else None

    def get_by_stationid(self, stationid: str) -> Airport | None:
        cursor = self._conn.execute(
            "SELECT * FROM airports WHERE stationid = ?", (stationid,)
        )
        row = cursor.fetchone()
        return self._row_to_airport(row, include_relations=True) if row else None

    def get_all(self) -> list[Airport]:
        cursor = self._conn.execute("SELECT * FROM airports ORDER BY stationid")
        return [self._row_to_airport(row) for row in cursor.fetchall()]

    def get_by_state(self, state: str) -> list[Airport]:
        cursor = self._conn.execute(
            "SELECT * FROM airports WHERE state = ? ORDER BY stationid", (state,)
        )
        return [self._row_to_airport(row) for row in cursor.fetchall()]

    def save(self, airport: Airport) -> Airport:
        if airport.id is None:
            cursor = self._conn.execute(
                """
				INSERT INTO airports (stationid, name, city, state, latitude, longitude)
				VALUES (?, ?, ?, ?, ?, ?)
			""",
                (
                    airport.stationid,
                    airport.name,
                    airport.city,
                    airport.state,
                    airport.latitude,
                    airport.longitude,
                ),
            )
            airport.id = cursor.lastrowid

            for runway in airport.runways:
                runway.airport_id = airport.id
                self._save_runway(runway)

            if airport.weather:
                airport.weather.airport_id = airport.id
                self._save_weather(airport.weather)
        else:
            self._conn.execute(
                """
				UPDATE airports 
				SET stationid = ?, name = ?, city = ?, state = ?, latitude = ?, longitude = ?
				WHERE id = ?
			""",
                (
                    airport.stationid,
                    airport.name,
                    airport.city,
                    airport.state,
                    airport.latitude,
                    airport.longitude,
                    airport.id,
                ),
            )

        self._conn.commit()
        return airport

    def delete(self, id: int) -> bool:
        cursor = self._conn.execute("DELETE FROM airports WHERE id = ?", (id,))
        self._conn.commit()
        return cursor.rowcount > 0

    def _save_runway(self, runway: Runway) -> Runway:
        cursor = self._conn.execute(
            """
			INSERT INTO runways (airport_id, identifier, length_ft, width_ft, surface)
			VALUES (?, ?, ?, ?, ?)
		""",
            (
                runway.airport_id,
                runway.identifier,
                runway.length_ft,
                runway.width_ft,
                runway.surface,
            ),
        )
        runway.id = cursor.lastrowid
        return runway

    def _save_weather(self, weather: WeatherReport) -> WeatherReport:
        cursor = self._conn.execute(
            """
			INSERT INTO weather_reports (airport_id, metar, taf, fetched_at)
			VALUES (?, ?, ?, ?)
		""",
            (
                weather.airport_id,
                weather.metar,
                weather.taf,
                weather.fetched_at.isoformat(),
            ),
        )
        weather.id = cursor.lastrowid
        return weather

    def _row_to_airport(
        self, row: sqlite3.Row, include_relations: bool = False
    ) -> Airport:
        airport = Airport(
            id=row["id"],
            stationid=row["stationid"],
            name=row["name"],
            city=row["city"] or "",
            state=row["state"] or "",
            latitude=row["latitude"],
            longitude=row["longitude"],
        )

        if include_relations and airport.id:
            airport.runways = self._get_runways(airport.id)
            airport.weather = self._get_latest_weather(airport.id)

        return airport

    def _get_runways(self, airport_id: int) -> list[Runway]:
        cursor = self._conn.execute(
            "SELECT * FROM runways WHERE airport_id = ? ORDER BY identifier",
            (airport_id,),
        )
        return [
            Runway(
                id=row["id"],
                airport_id=row["airport_id"],
                identifier=row["identifier"],
                length_ft=row["length_ft"],
                width_ft=row["width_ft"] or 0,
                surface=row["surface"] or "",
            )
            for row in cursor.fetchall()
        ]

    def _get_latest_weather(self, airport_id: int) -> WeatherReport | None:
        cursor = self._conn.execute(
            """
			SELECT * FROM weather_reports 
			WHERE airport_id = ? 
			ORDER BY fetched_at DESC LIMIT 1
		""",
            (airport_id,),
        )
        row = cursor.fetchone()
        if not row:
            return None

        fetched_at = row["fetched_at"]
        if isinstance(fetched_at, str):
            fetched_at = datetime.fromisoformat(fetched_at)

        return WeatherReport(
            id=row["id"],
            airport_id=row["airport_id"],
            metar=row["metar"],
            taf=row["taf"],
            fetched_at=fetched_at,
        )


# =============================================================================
# IN-MEMORY REPOSITORY (FOR TESTING)
# =============================================================================


class InMemoryAirportRepository(AirportRepository):
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

    def get_by_state(self, state: str) -> list[Airport]:
        return sorted(
            [a for a in self._airports.values() if a.state == state],
            key=lambda a: a.stationid,
        )

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


# =============================================================================
# UNIT OF WORK PATTERN
# =============================================================================


class UnitOfWork:
    def __init__(self, db_path: str | Path):
        self._db_path = str(db_path)
        self._conn: sqlite3.Connection | None = None
        self.airports: SQLiteAirportRepository | None = None

    def __enter__(self) -> "UnitOfWork":
        self._conn = sqlite3.connect(self._db_path)
        self._conn.execute("PRAGMA foreign_keys = ON")
        init_database(self._conn)
        self.airports = SQLiteAirportRepository(self._conn)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self._conn:
            if exc_type is None:
                self._conn.commit()
            else:
                self._conn.rollback()
            self._conn.close()
        return False

    def commit(self) -> None:
        if self._conn:
            self._conn.commit()

    def rollback(self) -> None:
        if self._conn:
            self._conn.rollback()


# =============================================================================
# QUERY BUILDER
# =============================================================================


class AirportQuery:
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
        self._conditions.append(
            "id IN (SELECT airport_id FROM runways WHERE length_ft >= ?)"
        )
        self._params.append(length_ft)
        return self

    def order_by(self, column: str) -> "AirportQuery":
        allowed = {"stationid", "name", "city", "state"}
        if column in allowed:
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


# =============================================================================
# MAIN DEMONSTRATION
# =============================================================================


def main() -> None:
    print("=" * 70)
    print("SQLITE DATABASE OPERATIONS DEMONSTRATION")
    print("=" * 70)

    # Use in-memory database for demo
    db_path = ":memory:"

    # -------------------------------------------------------------------------
    # 1. BASIC CONNECTION AND SCHEMA
    # -------------------------------------------------------------------------

    print("\n1. DATABASE CONNECTION AND SCHEMA")
    print("-" * 40)

    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    init_database(conn)

    cursor = conn.execute("""
		SELECT name FROM sqlite_master 
		WHERE type='table' AND name NOT LIKE 'sqlite_%'
		ORDER BY name
	""")
    tables = [row["name"] for row in cursor.fetchall()]
    print(f"  Tables created: {', '.join(tables)}")

    # -------------------------------------------------------------------------
    # 2. BASIC CRUD OPERATIONS
    # -------------------------------------------------------------------------

    print("\n2. BASIC CRUD OPERATIONS")
    print("-" * 40)

    # INSERT
    cursor = conn.execute(
        """
		INSERT INTO airports (stationid, name, city, state, latitude, longitude)
		VALUES (?, ?, ?, ?, ?, ?)
	""",
        (
            "KAMA",
            "Rick Husband Amarillo International Airport",
            "Amarillo",
            "TX",
            35.2194,
            -101.7059,
        ),
    )
    kama_id = cursor.lastrowid
    print(f"  INSERT: Created KAMA with ID {kama_id}")

    # INSERT runways
    conn.execute(
        """
		INSERT INTO runways (airport_id, identifier, length_ft, width_ft, surface)
		VALUES (?, ?, ?, ?, ?)
	""",
        (kama_id, "04/22", 13502, 200, "concrete"),
    )
    conn.execute(
        """
		INSERT INTO runways (airport_id, identifier, length_ft, width_ft, surface)
		VALUES (?, ?, ?, ?, ?)
	""",
        (kama_id, "13/31", 7898, 150, "asphalt"),
    )
    conn.commit()
    print(f"  INSERT: Added 2 runways to KAMA")

    # SELECT with JOIN
    cursor = conn.execute(
        """
		SELECT a.stationid, r.identifier, r.length_ft
		FROM airports a
		JOIN runways r ON a.id = r.airport_id
		WHERE a.stationid = ?
	""",
        ("KAMA",),
    )
    print(f"  SELECT JOIN: Runways for KAMA:")
    for row in cursor.fetchall():
        print(f"    {row['identifier']}: {row['length_ft']}ft")

    # UPDATE
    conn.execute(
        "UPDATE airports SET name = ? WHERE stationid = ?",
        ("Amarillo International Airport", "KAMA"),
    )
    conn.commit()
    print(f"  UPDATE: Updated KAMA name")

    conn.close()

    # -------------------------------------------------------------------------
    # 3. REPOSITORY PATTERN
    # -------------------------------------------------------------------------

    print("\n3. REPOSITORY PATTERN")
    print("-" * 40)

    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    init_database(conn)
    repo = SQLiteAirportRepository(conn)

    # Create airports with runways
    airports_data = [
        Airport(
            id=None,
            stationid="KAMA",
            name="Rick Husband Amarillo International Airport",
            city="Amarillo",
            state="TX",
            latitude=35.2194,
            longitude=-101.7059,
            runways=[
                Runway(None, 0, "04/22", 13502, 200, "concrete"),
                Runway(None, 0, "13/31", 7898, 150, "asphalt"),
            ],
            weather=WeatherReport(None, 0, "KAMA 121755Z 36010KT 10SM CLR", None),
        ),
        Airport(
            id=None,
            stationid="KLBB",
            name="Lubbock Preston Smith International Airport",
            city="Lubbock",
            state="TX",
            latitude=33.6636,
            longitude=-101.8228,
            runways=[
                Runway(None, 0, "17R/35L", 11500, 150, "concrete"),
            ],
        ),
        Airport(
            id=None,
            stationid="KMAF",
            name="Midland International Air and Space Port",
            city="Midland",
            state="TX",
            latitude=31.9425,
            longitude=-102.2019,
            runways=[
                Runway(None, 0, "10/28", 9501, 150, "concrete"),
            ],
        ),
    ]

    for airport in airports_data:
        saved = repo.save(airport)
        print(f"  Saved: {saved.stationid} with ID {saved.id}")

    # Query by stationid
    kama = repo.get_by_stationid("KAMA")
    if kama:
        print(f"\n  Retrieved KAMA:")
        print(f"    Name: {kama.name}")
        print(f"    Runways: {len(kama.runways)}")
        print(f"    Weather: {kama.weather.metar if kama.weather else 'None'}")

    # Query by state
    texas_airports = repo.get_by_state("TX")
    print(f"\n  Texas airports: {len(texas_airports)}")
    for airport in texas_airports:
        print(f"    {airport.stationid}: {airport.name}")

    conn.close()

    # -------------------------------------------------------------------------
    # 4. UNIT OF WORK PATTERN
    # -------------------------------------------------------------------------

    print("\n4. UNIT OF WORK PATTERN")
    print("-" * 40)

    with UnitOfWork(":memory:") as uow:
        airport = Airport(
            id=None,
            stationid="KDFW",
            name="Dallas/Fort Worth International Airport",
            city="Dallas",
            state="TX",
            runways=[
                Runway(None, 0, "17L/35R", 13401, 200, "concrete"),
                Runway(None, 0, "17R/35L", 13401, 200, "concrete"),
            ],
        )
        saved = uow.airports.save(airport)
        print(f"  Created DFW with {len(saved.runways)} runways in transaction")

        uow.airports.save(
            Airport(None, "KHOU", "William P. Hobby Airport", "Houston", "TX")
        )
        uow.airports.save(
            Airport(None, "KSAT", "San Antonio International", "San Antonio", "TX")
        )

        all_airports = uow.airports.get_all()
        print(f"  Total airports: {len(all_airports)}")

    print("  Transaction committed")

    # -------------------------------------------------------------------------
    # 5. QUERY BUILDER
    # -------------------------------------------------------------------------

    print("\n5. QUERY BUILDER")
    print("-" * 40)

    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    init_database(conn)

    repo = SQLiteAirportRepository(conn)
    for airport in airports_data:
        airport.id = None
        for r in airport.runways:
            r.id = None
        if airport.weather:
            airport.weather.id = None
        repo.save(airport)

    query = AirportQuery().in_state("TX").with_min_runway(10000).order_by("name")

    sql, params = query.build()
    print(f"  Query: {sql}")
    print(f"  Params: {params}")

    cursor = conn.execute(sql, params)
    results = cursor.fetchall()
    print(f"\n  Results (TX airports with runway >= 10000ft):")
    for row in results:
        print(f"    {row['stationid']}: {row['name']}")

    conn.close()

    # -------------------------------------------------------------------------
    # 6. TRANSACTIONS AND ERROR HANDLING
    # -------------------------------------------------------------------------

    print("\n6. TRANSACTIONS AND ERROR HANDLING")
    print("-" * 40)

    conn = sqlite3.connect(":memory:")
    conn.execute("PRAGMA foreign_keys = ON")
    init_database(conn)

    try:
        cursor = conn.cursor()
        cursor.execute(
            """
			INSERT INTO airports (stationid, name, city, state)
			VALUES (?, ?, ?, ?)
		""",
            ("KDEN", "Denver International", "Denver", "CO"),
        )
        print("  Inserted KDEN")

        cursor.execute(
            """
			INSERT INTO airports (stationid, name, city, state)
			VALUES (?, ?, ?, ?)
		""",
            ("KDEN", "Duplicate Denver", "Denver", "CO"),
        )

        conn.commit()

    except sqlite3.IntegrityError as e:
        conn.rollback()
        print(f"  IntegrityError caught: {e}")
        print("  Transaction rolled back")

    cursor = conn.execute("SELECT COUNT(*) FROM airports")
    count = cursor.fetchone()[0]
    print(f"  Airports after rollback: {count}")

    conn.close()

    # -------------------------------------------------------------------------
    # 7. IN-MEMORY REPOSITORY (FOR TESTING)
    # -------------------------------------------------------------------------

    print("\n7. IN-MEMORY REPOSITORY (FOR TESTING)")
    print("-" * 40)

    test_repo = InMemoryAirportRepository()

    test_repo.save(Airport(None, "TEST1", "Test Airport 1", "City", "ST"))
    test_repo.save(Airport(None, "TEST2", "Test Airport 2", "City", "ST"))

    print(f"  Saved 2 test airports")
    print(f"  get_all() returns: {len(test_repo.get_all())} airports")

    found = test_repo.get_by_stationid("TEST1")
    print(f"  Found by stationid: {found.name if found else 'None'}")

    deleted = test_repo.delete(1)
    print(f"  Deleted ID 1: {deleted}")
    print(f"  Remaining: {len(test_repo.get_all())} airports")

    print("\n" + "=" * 70)
    print("DEMONSTRATION COMPLETE")
    print("=" * 70)


if __name__ == "__main__":
    main()
