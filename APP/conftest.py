import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from orm import metadata, start_mappers

@pytest.fixture(scope='session')
def the_db():
    # engine = create_engine('sqlite+pysqlite:///test.db', echo=True)
    engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)

    metadata.create_all(engine)
    start_mappers()
    return engine

@pytest.fixture(scope='session')
def session(the_db):
    Session = sessionmaker(bind=the_db)
    the_session = Session()
    return the_session
