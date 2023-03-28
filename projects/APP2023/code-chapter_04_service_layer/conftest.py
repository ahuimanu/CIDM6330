# pylint: disable=redefined-outer-name
import time
from pathlib import Path

import pytest
import requests
from requests.exceptions import ConnectionError
from sqlalchemy.exc import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.sql import delete, insert, select, text
from sqlalchemy.orm import sessionmaker, clear_mappers

import config
from flask_app import create_app
from model import Batch
from orm import mapper_registry, start_mappers, batches


# chapter reworked to follow
# https://flask.palletsprojects.com/en/2.2.x/patterns/appfactories/#application-factories
# and
# https://flask.palletsprojects.com/en/2.2.x/testing/#testing-flask-applications
# P&G might be too fixated on Docker containers with their example.


@pytest.fixture
def in_memory_db():
    engine = create_engine(f"sqlite:///:memory:")
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def file_sqlite_db():
    engine = create_engine(config.get_sqlite_filedb_uri())
    mapper_registry.metadata.create_all(engine)
    return engine


@pytest.fixture
def session(file_sqlite_db):
    start_mappers()
    yield sessionmaker(bind=file_sqlite_db)()
    clear_mappers()


@pytest.fixture
def flask_api(session):
    app = create_app()
    app.config.update({"TESTING": True})
    return app


@pytest.fixture
def test_client(flask_api):
    return flask_api.test_client()


# def wait_for_postgres_to_come_up(engine):
#     deadline = time.time() + 10
#     while time.time() < deadline:
#         try:
#             return engine.connect()
#         except OperationalError:
#             time.sleep(0.5)
#     pytest.fail("Postgres never came up")


# def wait_for_webapp_to_come_up():
#     deadline = time.time() + 10
#     url = config.get_api_url()
#     while time.time() < deadline:
#         try:
#             return requests.get(url)
#         except ConnectionError:
#             time.sleep(0.5)
#     pytest.fail("API never came up")


# @pytest.fixture(scope="session")
# def postgres_db():
#     engine = create_engine(config.get_postgres_uri())
#     wait_for_postgres_to_come_up(engine)
#     mapper_registry.metadata.create_all(engine)
#     return engine


# @pytest.fixture
# def postgres_session(postgres_db):
#     start_mappers()
#     yield sessionmaker(bind=postgres_db)()
#     clear_mappers()


@pytest.fixture
def add_stock(session):
    # take care and note that this fixture takes care of adding in records to the database.
    batches_added = set()
    skus_added = set()

    def _add_stock(lines):
        print(lines)
        for ref, sku, qty, eta in lines:
            # session.execute(
            #     text(
            #         "INSERT INTO batches (reference, sku, _purchased_quantity, eta)"
            #         " VALUES (:ref, :sku, :qty, :eta)"
            #     ),
            #     dict(ref=ref, sku=sku, qty=qty, eta=eta),
            # )
            # [[batch_id]] = session.scalars(
            #     text("SELECT id FROM batches WHERE reference=:ref AND sku=:sku"),
            #     dict(ref=ref, sku=sku),
            # )
            session.execute(
                insert(batches).values(
                    reference=ref, sku=sku, _purchased_quantity=qty, eta=eta
                )
            )
            batch_id = session.scalars(
                select(Batch).where(Batch.reference == ref).where(Batch.sku == sku)
            ).first()
            print(batch_id.reference)
            print(batch_id.sku)
            batches_added.add(batch_id.reference)
            skus_added.add(batch_id.sku)
        session.commit()
        session.close()

    yield _add_stock

    for batch_id in batches_added:
        session.execute(
            text("DELETE FROM allocations WHERE batch_id=:batch_id"),
            dict(batch_id=batch_id),
        )
        session.execute(
            text("DELETE FROM batches WHERE id=:batch_id"),
            dict(batch_id=batch_id),
        )
    for sku in skus_added:
        session.execute(
            text("DELETE FROM order_lines WHERE sku=:sku"),
            dict(sku=sku),
        )

    session.commit()


# @pytest.fixture
# def restart_api():
#     (Path(__file__).parent / "flask_app.py").touch()
#     time.sleep(0.5)
