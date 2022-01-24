import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from deckman.model.artist import Artist
from deckman.orm.artist import metadata_obj, SQLAlchemyArtistRepo


@pytest.fixture(scope="session")
def engine():
    return create_engine("sqlite:///:memory:")


@pytest.fixture(scope="session")
def tables(engine):
    metadata_obj.create_all(engine)
    yield
    metadata_obj.drop_all(engine)


@pytest.fixture
def session(engine, tables):
    session = Session(engine)
    yield session
    session.rollback()
    session.close()


@pytest.fixture
def insert_artist(session):
    session.execute(
        "INSERT INTO artists ('musicbrainz_id', 'name') "
        "VALUES ('123', 'The Fake Artist')"
    )
    session.flush()


def test_artist_repo_can_add(session):
    artist = Artist(1, "123", "The Fake Artist", "Fake Artist, The")
    repo = SQLAlchemyArtistRepo(session)
    repo.add(artist)
    session.flush()

    rows = session.execute("SELECT musicbrainz_id, name FROM artists")
    assert list(rows) == [("123", "The Fake Artist")]


def test_artist_repo_can_list(session, insert_artist):
    repo = SQLAlchemyArtistRepo(session)
    artists = repo.list()
    assert type(artists[0]) == Artist
    assert artists[0].name == "The Fake Artist"


def test_artist_repo_can_get(session, insert_artist):
    repo = SQLAlchemyArtistRepo(session)
    artist = repo.get(1)
    assert artist.name == "The Fake Artist"
