import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import clear_mappers, sessionmaker

# only needed for test_orm.py
from orm import metadata, start_mappers


# @pytest.fixture(scope='session')
@pytest.fixture
def the_db():
    # engine = create_engine('sqlite+pysqlite:///test.db', echo=True)
    engine = create_engine('sqlite+pysqlite:///:memory:', echo=True)

    metadata.create_all(engine)
    return engine

@pytest.fixture
def session(the_db):
    start_mappers()
    # Session = sessionmaker(bind=the_db)
    # the_session = Session()
    yield sessionmaker(bind=the_db)()
    clear_mappers()
