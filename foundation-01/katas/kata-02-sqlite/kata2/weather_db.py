from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from collections.abc import Sequence
    from pathlib import Path


@dataclass(frozen=True)
class Station:
    station_id: str
    name: str
    state: str


@dataclass(frozen=True)
class Observation:
    station_id: str
    obs_date: str  # ISO date string YYYY-MM-DD
    temperature_c: float


def connect(db_path: Path) -> sqlite3.Connection:
    """
    Create a SQLite connection. Caller is responsible for closing.
    """
    db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def create_schema(conn: sqlite3.Connection) -> None:
    """
    Create tables for stations and observations (2 related tables).
    """
    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS stations (
            station_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            state TEXT NOT NULL
        )
        """
    )

    conn.execute(
        """
        CREATE TABLE IF NOT EXISTS observations (
            obs_id INTEGER PRIMARY KEY AUTOINCREMENT,
            station_id TEXT NOT NULL,
            obs_date TEXT NOT NULL,
            temperature_c REAL NOT NULL,
            FOREIGN KEY (station_id) REFERENCES stations(station_id)
        )
        """
    )
    conn.commit()


# ---------- CRUD: Stations ----------


def insert_station(conn: sqlite3.Connection, station: Station) -> None:
    """
    Insert a station row (parameterized query).
    """
    conn.execute(
        "INSERT INTO stations (station_id, name, state) VALUES (?, ?, ?)",
        (station.station_id, station.name, station.state),
    )
    conn.commit()


def get_station(conn: sqlite3.Connection, station_id: str) -> Station | None:
    """
    Fetch a station by ID.
    """
    cur = conn.execute(
        "SELECT station_id, name, state FROM stations WHERE station_id = ?",
        (station_id,),
    )
    row = cur.fetchone()
    if row is None:
        return None
    return Station(row["station_id"], row["name"], row["state"])


def list_stations(conn: sqlite3.Connection) -> list[Station]:
    """
    List all stations.
    """
    cur = conn.execute(
        "SELECT station_id, name, state FROM stations ORDER BY station_id"
    )
    return [Station(r["station_id"], r["name"], r["state"]) for r in cur.fetchall()]


def update_station_name(
    conn: sqlite3.Connection, station_id: str, new_name: str
) -> int:
    """
    Update station name. Returns number of rows updated.
    """
    cur = conn.execute(
        "UPDATE stations SET name = ? WHERE station_id = ?",
        (new_name, station_id),
    )
    conn.commit()
    return cur.rowcount


def delete_station(conn: sqlite3.Connection, station_id: str) -> int:
    """
    Delete station by ID. Returns number of rows deleted.
    """
    cur = conn.execute(
        "DELETE FROM stations WHERE station_id = ?",
        (station_id,),
    )
    conn.commit()
    return cur.rowcount


# ---------- CRUD: Observations ----------


def insert_observation(conn: sqlite3.Connection, obs: Observation) -> None:
    """
    Insert an observation (parameterized query).
    """
    conn.execute(
        """
        INSERT INTO observations (station_id, obs_date, temperature_c)
        VALUES (?, ?, ?)
        """,
        (obs.station_id, obs.obs_date, obs.temperature_c),
    )
    conn.commit()


def list_observations_for_station(
    conn: sqlite3.Connection, station_id: str, start_date: str, end_date: str
) -> list[Observation]:
    """
    List observations for a station between start_date and end_date.

    The boundaries are inclusive because the query uses BETWEEN.
    """
    cur = conn.execute(
        """
        SELECT station_id, obs_date, temperature_c
        FROM observations
        WHERE station_id = ?
          AND obs_date BETWEEN ? AND ?
        ORDER BY obs_date
        """,
        (station_id, start_date, end_date),
    )
    return [
        Observation(r["station_id"], r["obs_date"], r["temperature_c"])
        for r in cur.fetchall()
    ]


def update_observation_temp(
    conn: sqlite3.Connection, station_id: str, obs_date: str, new_temp: float
) -> int:
    """
    Update temperature for a specific station/date. Returns number of rows updated.
    """
    cur = conn.execute(
        """
        UPDATE observations
        SET temperature_c = ?
        WHERE station_id = ? AND obs_date = ?
        """,
        (new_temp, station_id, obs_date),
    )
    conn.commit()
    return cur.rowcount


def delete_observations_for_station(conn: sqlite3.Connection, station_id: str) -> int:
    """
    Delete all observations for a station. Returns number of rows deleted.
    """
    cur = conn.execute(
        "DELETE FROM observations WHERE station_id = ?",
        (station_id,),
    )
    conn.commit()
    return cur.rowcount


# ---------- Join query (meaningful query) ----------


def get_station_daily_summary(
    conn: sqlite3.Connection,
    start_date: str,
    end_date: str,
    temp_threshold_c: float,
) -> list[dict[str, Any]]:
    """
    Join stations and observations to return a meaningful result:
    stations that had observations >= threshold within date range,
    along with average temperature over that range.

    Returns list of dicts: station_id, name, state, avg_temp, obs_count
    """
    cur = conn.execute(
        """
        SELECT
            s.station_id,
            s.name,
            s.state,
            AVG(o.temperature_c) AS avg_temp,
            COUNT(*) AS obs_count
        FROM stations s
        JOIN observations o
          ON o.station_id = s.station_id
        WHERE o.obs_date BETWEEN ? AND ?
          AND o.temperature_c >= ?
        GROUP BY s.station_id, s.name, s.state
        ORDER BY avg_temp DESC
        """,
        (start_date, end_date, temp_threshold_c),
    )
    return [dict(row) for row in cur.fetchall()]


# ---------- Seed data ----------


def seed(conn: sqlite3.Connection) -> None:
    """
    Populate the database with sample data.
    Safe to run multiple times (clears existing rows).
    """
    conn.execute("DELETE FROM observations")
    conn.execute("DELETE FROM stations")

    stations = [
        Station("ST001", "Canyon Station", "TX"),
        Station("ST002", "Amarillo Station", "TX"),
        Station("ST003", "Lubbock Station", "TX"),
    ]
    for s in stations:
        conn.execute(
            "INSERT INTO stations (station_id, name, state) VALUES (?, ?, ?)",
            (s.station_id, s.name, s.state),
        )

    observations = [
        Observation("ST001", "2026-02-01", 12.3),
        Observation("ST001", "2026-02-02", 11.0),
        Observation("ST001", "2026-02-03", 9.8),
        Observation("ST002", "2026-02-01", 5.2),
        Observation("ST002", "2026-02-02", 6.1),
        Observation("ST003", "2026-02-01", 18.7),
        Observation("ST003", "2026-02-02", 17.9),
        Observation("ST003", "2026-02-03", 16.2),
    ]
    for o in observations:
        conn.execute(
            """
            INSERT INTO observations (station_id, obs_date, temperature_c)
            VALUES (?, ?, ?)
            """,
            (o.station_id, o.obs_date, o.temperature_c),
        )

    conn.commit()


# ---------- Stretch: Index + explain plan ----------


def create_indexes(conn: sqlite3.Connection) -> None:
    """
    Create an index to speed up date and station lookup.
    """
    conn.execute(
        """
        CREATE INDEX IF NOT EXISTS idx_obs_station_date
        ON observations(station_id, obs_date)
        """
    )
    conn.commit()


def explain_query_plan(
    conn: sqlite3.Connection, sql: str, params: Sequence[object] = ()
) -> list[tuple]:
    """
    Run EXPLAIN QUERY PLAN for a given SQL statement and params.
    Returns raw rows for inspection.
    """
    cur = conn.execute(f"EXPLAIN QUERY PLAN {sql}", params)
    return [tuple(r) for r in cur.fetchall()]
