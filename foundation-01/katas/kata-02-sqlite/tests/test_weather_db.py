import sqlite3
from pathlib import Path

import pytest
from kata2.weather_db import (
    Observation,
    Station,
    connect,
    create_indexes,
    create_schema,
    delete_observations_for_station,
    delete_station,
    explain_query_plan,
    get_station,
    get_station_daily_summary,
    insert_observation,
    insert_station,
    list_observations_for_station,
    list_stations,
    seed,
    update_observation_temp,
    update_station_name,
)


@pytest.fixture
def db_path(tmp_path: Path) -> Path:
    return tmp_path / "weather_test.db"


@pytest.fixture
def conn(db_path: Path):
    connection = connect(db_path)
    create_schema(connection)
    try:
        yield connection
    finally:
        connection.close()


@pytest.fixture
def seeded_conn(conn):
    seed(conn)
    return conn


def test_connect_enables_foreign_keys(conn):
    foreign_keys = conn.execute("PRAGMA foreign_keys").fetchone()[0]
    assert foreign_keys == 1


def test_create_schema_creates_expected_tables(conn):
    rows = conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table'
          AND name IN ('stations', 'observations')
        ORDER BY name
        """
    ).fetchall()

    assert [row["name"] for row in rows] == ["observations", "stations"]


def test_create_schema_is_idempotent(conn):
    create_schema(conn)

    rows = conn.execute(
        "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'stations'"
    ).fetchall()
    assert len(rows) == 1


def test_insert_and_get_station(conn):
    station = Station("ST100", "Test Station", "TX")

    insert_station(conn, station)

    assert get_station(conn, "ST100") == station


def test_get_station_returns_none_for_missing_id(conn):
    assert get_station(conn, "MISSING") is None


def test_list_stations_returns_sorted_by_station_id(conn):
    insert_station(conn, Station("ST200", "Second", "TX"))
    insert_station(conn, Station("ST100", "First", "TX"))
    insert_station(conn, Station("ST300", "Third", "TX"))

    stations = list_stations(conn)

    assert [station.station_id for station in stations] == ["ST100", "ST200", "ST300"]


def test_update_station_name_returns_one_for_existing_station(conn):
    insert_station(conn, Station("ST100", "Old Name", "TX"))

    updated = update_station_name(conn, "ST100", "New Name")

    assert updated == 1
    assert get_station(conn, "ST100") == Station("ST100", "New Name", "TX")


def test_update_station_name_returns_zero_for_missing_station(conn):
    assert update_station_name(conn, "MISSING", "New Name") == 0


def test_delete_station_returns_one_for_existing_station_without_observations(conn):
    insert_station(conn, Station("ST100", "Solo Station", "TX"))

    deleted = delete_station(conn, "ST100")

    assert deleted == 1
    assert get_station(conn, "ST100") is None


def test_delete_station_returns_zero_for_missing_station(conn):
    assert delete_station(conn, "MISSING") == 0


def test_insert_station_duplicate_primary_key_raises_integrity_error(conn):
    insert_station(conn, Station("ST100", "Original", "TX"))

    with pytest.raises(sqlite3.IntegrityError):
        insert_station(conn, Station("ST100", "Duplicate", "TX"))


def test_insert_observation_and_list_for_station_in_date_range(conn):
    insert_station(conn, Station("ST100", "Test Station", "TX"))
    insert_observation(conn, Observation("ST100", "2026-02-01", 12.3))
    insert_observation(conn, Observation("ST100", "2026-02-02", 10.0))

    observations = list_observations_for_station(
        conn, "ST100", "2026-02-01", "2026-02-02"
    )

    assert observations == [
        Observation("ST100", "2026-02-01", 12.3),
        Observation("ST100", "2026-02-02", 10.0),
    ]


def test_list_observations_for_station_includes_between_boundaries(seeded_conn):
    observations = list_observations_for_station(
        seeded_conn, "ST001", "2026-02-01", "2026-02-03"
    )

    assert [obs.obs_date for obs in observations] == [
        "2026-02-01",
        "2026-02-02",
        "2026-02-03",
    ]


@pytest.mark.parametrize(
    ("station_id", "start_date", "end_date", "expected_dates"),
    [
        (
            "ST001",
            "2026-02-01",
            "2026-02-03",
            ["2026-02-01", "2026-02-02", "2026-02-03"],
        ),
        ("ST001", "2026-02-02", "2026-02-02", ["2026-02-02"]),
        ("ST001", "2026-02-02", "2026-02-03", ["2026-02-02", "2026-02-03"]),
        ("ST001", "2026-03-01", "2026-03-31", []),
        ("ST001", "2026-02-03", "2026-02-01", []),
    ],
)
def test_list_observations_for_station_parametrized_ranges(
    seeded_conn, station_id, start_date, end_date, expected_dates
):
    observations = list_observations_for_station(
        seeded_conn, station_id, start_date, end_date
    )

    assert [obs.obs_date for obs in observations] == expected_dates


def test_update_observation_temp_returns_one_for_existing_row(conn):
    insert_station(conn, Station("ST100", "Test Station", "TX"))
    insert_observation(conn, Observation("ST100", "2026-02-01", 12.3))

    updated = update_observation_temp(conn, "ST100", "2026-02-01", 15.5)

    assert updated == 1
    assert list_observations_for_station(conn, "ST100", "2026-02-01", "2026-02-01") == [
        Observation("ST100", "2026-02-01", 15.5)
    ]


def test_update_observation_temp_returns_zero_for_missing_row(conn):
    insert_station(conn, Station("ST100", "Test Station", "TX"))

    assert update_observation_temp(conn, "ST100", "2026-02-01", 15.5) == 0


def test_delete_observations_for_station_returns_count(seeded_conn):
    deleted = delete_observations_for_station(seeded_conn, "ST003")

    remaining = list_observations_for_station(
        seeded_conn, "ST003", "2026-02-01", "2026-02-03"
    )

    assert deleted == 3
    assert remaining == []


def test_delete_observations_for_station_returns_zero_when_none_exist(conn):
    insert_station(conn, Station("ST100", "Test Station", "TX"))

    assert delete_observations_for_station(conn, "ST100") == 0


def test_insert_observation_for_missing_station_raises_integrity_error(conn):
    with pytest.raises(sqlite3.IntegrityError):
        insert_observation(conn, Observation("MISSING", "2026-02-01", 12.3))


def test_delete_station_with_existing_observations_raises_integrity_error(seeded_conn):
    with pytest.raises(sqlite3.IntegrityError):
        delete_station(seeded_conn, "ST001")


@pytest.mark.parametrize(
    "station",
    [
        Station("ST100", None, "TX"),
        Station("ST100", "Name", None),
    ],
)
def test_insert_station_with_none_not_null_fields_raises_integrity_error(conn, station):
    with pytest.raises(sqlite3.IntegrityError):
        insert_station(conn, station)


def test_insert_station_with_none_station_id_matches_current_behavior(conn):
    station = Station(None, "Name", "TX")
    insert_station(conn, station)

    stations = list_stations(conn)
    assert len(stations) == 1
    assert stations[0].station_id is None


@pytest.mark.parametrize(
    "observation",
    [
        Observation(None, "2026-02-01", 10.0),
        Observation("ST100", None, 10.0),
        Observation("ST100", "2026-02-01", None),
    ],
)
def test_insert_observation_with_none_required_field_raises_integrity_error(
    conn, observation
):
    insert_station(conn, Station("ST100", "Test Station", "TX"))

    with pytest.raises((sqlite3.IntegrityError, sqlite3.ProgrammingError)):
        insert_observation(conn, observation)


def test_insert_station_with_empty_strings_currently_succeeds(conn):
    insert_station(conn, Station("", "", ""))

    assert get_station(conn, "") == Station("", "", "")


def test_get_station_daily_summary_returns_expected_shape_and_order(seeded_conn):
    summary = get_station_daily_summary(seeded_conn, "2026-02-01", "2026-02-03", 10.0)

    assert [row["station_id"] for row in summary] == ["ST003", "ST001"]
    assert set(summary[0]) == {"station_id", "name", "state", "avg_temp", "obs_count"}


def test_get_station_daily_summary_returns_empty_when_nothing_meets_threshold(
    seeded_conn,
):
    summary = get_station_daily_summary(seeded_conn, "2026-02-01", "2026-02-03", 100.0)

    assert summary == []


def test_get_station_daily_summary_uses_only_qualifying_rows_in_average(seeded_conn):
    summary = get_station_daily_summary(seeded_conn, "2026-02-01", "2026-02-03", 10.0)

    station_rows = {row["station_id"]: row for row in summary}

    assert station_rows["ST001"]["avg_temp"] == pytest.approx((12.3 + 11.0) / 2)
    assert station_rows["ST001"]["obs_count"] == 2
    assert station_rows["ST003"]["avg_temp"] == pytest.approx((18.7 + 17.9 + 16.2) / 3)
    assert station_rows["ST003"]["obs_count"] == 3


def test_get_station_daily_summary_start_date_after_end_date_returns_empty(seeded_conn):
    summary = get_station_daily_summary(seeded_conn, "2026-02-03", "2026-02-01", 0.0)

    assert summary == []


def test_seed_populates_expected_counts(conn):
    seed(conn)

    station_count = conn.execute("SELECT COUNT(*) FROM stations").fetchone()[0]
    observation_count = conn.execute("SELECT COUNT(*) FROM observations").fetchone()[0]

    assert station_count == 3
    assert observation_count == 8


def test_seed_is_repeatable_and_resets_existing_data(conn):
    insert_station(conn, Station("EXTRA", "Extra Station", "TX"))
    seed(conn)
    insert_station(conn, Station("TEMP", "Temporary Station", "TX"))

    seed(conn)

    station_ids = [station.station_id for station in list_stations(conn)]
    assert station_ids == ["ST001", "ST002", "ST003"]


def test_create_indexes_runs_successfully(seeded_conn):
    create_indexes(seeded_conn)

    index_names = seeded_conn.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'index'
          AND name = 'idx_obs_station_date'
        """
    ).fetchall()

    assert len(index_names) == 1


def test_explain_query_plan_returns_rows(seeded_conn):
    rows = explain_query_plan(
        seeded_conn,
        """
        SELECT station_id, obs_date
        FROM observations
        WHERE station_id = ?
          AND obs_date BETWEEN ? AND ?
        """,
        ("ST001", "2026-02-01", "2026-02-03"),
    )

    assert rows
    assert all(isinstance(row, tuple) for row in rows)
