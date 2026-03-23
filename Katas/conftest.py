import sqlite3
import pytest

from pathlib import Path

try:
    # Prefer the project's sqlite helper if available
    from Katas.Kata2 import sqlite_kata
except Exception:
    sqlite_kata = None


@pytest.fixture
def tmp_sqlite_db(tmp_path):
    """Create an initialized SQLite DB file and return its path as string.

    Tests can use this fixture to get a ready-to-use database path:
        def test_x(tmp_sqlite_db):
            # use tmp_sqlite_db (str path)
    """
    db_path = tmp_path / "test_kata.db"
    if sqlite_kata and hasattr(sqlite_kata, "connect_db"):
        conn = sqlite_kata.connect_db(str(db_path))
        # initialize schema if helper provided
        if hasattr(sqlite_kata, "init_database"):
            sqlite_kata.init_database(conn)
        conn.close()
    else:
        # fallback: create an empty sqlite file
        conn = sqlite3.connect(str(db_path))
        conn.close()

    yield str(db_path)
