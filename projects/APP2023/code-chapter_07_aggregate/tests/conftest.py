# pylint: disable=redefined-outer-name
import os
import time
from pathlib import Path

import pytest
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.sql import delete, insert, select, text
from sqlalchemy.orm import sessionmaker, clear_mappers

from allocation import config
from allocation.entrypoints.flask_app import create_app
from allocation.domain.model import Batch
from allocation.adapters.orm import mapper_registry, start_mappers, batches


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def file_sqlite_db():
    engine = create_engine(config.get_sqlite_filedb_uri())
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session_factory(file_sqlite_db):
    # setup
    start_mappers()
    # what is "yield?"
    # Python Generators: https://realpython.com/introduction-to-python-generators/
    yield sessionmaker(bind=file_sqlite_db)()
    # teardown
    clear_mappers()
    file_sqlite_db.dispose()

    # remove db
    path = Path(__file__).parent
    os.remove(path / "allocation.db")


@pytest.fixture
def session(session_factory):
    return session_factory

@pytest.fixture
def test_client(flask_api):
    return flask_api.test_client()

@pytest.fixture
def flask_api(session):
    app = create_app()
    app.config.update({"TESTING": True})
    return app
