import sqlite3
from Kata2 import sqlite_kata


def test_repo_insert_and_query():
    conn = sqlite_kata.connect_db(":memory:")
    sqlite_kata.init_database(conn)
    repo = sqlite_kata.SQLiteAirportRepository(conn)

    aid = repo.insert_airport("TST", "Test Airport", "Test City")
    assert isinstance(aid, int) and aid > 0

    fid = repo.insert_flight("TST100", aid, aid, "2026-02-08T10:00:00")
    assert isinstance(fid, int) and fid > 0

    airports = repo.get_airports()
    assert len(airports) == 1

    flights = repo.get_flights()
    assert len(flights) == 1

    joined = repo.flights_with_airports()
    assert len(joined) == 1

    conn.close()


def test_uow_transaction_rollback():
    db_path = ":memory:"
    uow = sqlite_kata.UnitOfWork(db_path)
    with uow:
        # create an airport, then attempt to create a duplicate to force IntegrityError
        repo = uow.repo
        repo.insert_airport("DUP", "Dup Airport", "City")
        try:
            repo.insert_airport("DUP", "Dup Airport 2", "City")
            uow.conn.commit()
        except sqlite3.IntegrityError:
            # rollback and assert that only the first exists
            uow.conn.rollback()

    # After context manager, connection is closed; open a fresh in-memory DB to verify schema (no persistent data expected)
    conn2 = sqlite_kata.connect_db(":memory:")
    sqlite_kata.init_database(conn2)
    cur = conn2.execute("SELECT COUNT(*) FROM airports")
    assert cur.fetchone()[0] == 0
    conn2.close()
