import pytest
from sqlalchemy import create_engine

from deckman.database.tables import metadata_obj


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite+pysqlite:///:memory:", future=True)


@pytest.fixture(scope="session")
def create_tables(engine):
    metadata_obj.create_all(engine)
    yield engine
    metadata_obj.drop_all(engine)


@pytest.fixture
def db_connection(engine, create_tables):
    with engine.connect() as conn:
        yield conn
        conn.rollback()

@pytest.fixture(scope="session")
def initial_data(engine):
    with engine.connect() as conn:
        with open("src/deckman/database/initial/settings_lossy.json") as f:
            data = json.load(f)
            conn.execute(settings_lossy.insert(), data)
            conn.commit()
