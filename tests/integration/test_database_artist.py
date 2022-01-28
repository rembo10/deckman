import pytest
from sqlalchemy import text

from deckman.database.repos import SQLAlchemyArtistRepo
from deckman.model.artist import Artist
from deckman.model.exceptions import AlreadyExistsError, NotFoundError


@pytest.fixture
def repo(db_connection):
    return SQLAlchemyArtistRepo(db_connection)


@pytest.fixture
def setup_artists(db_connection):
    db_connection.execute(
        text(
            "INSERT INTO artists ('id', 'musicbrainz_id', 'name') VALUES "
            "(1, '456', 'The Fake Artist'), "
            "(2, '789', 'The 2nd Fake Artist')"
        )
    )


def test_can_create(repo, db_connection):
    artist = repo.create(musicbrainz_id="123")

    rows = db_connection.execute(
        text("SELECT id, musicbrainz_id FROM artists")
    )

    assert list(rows) == [(1, "123")]
    assert artist.id == 1
    assert artist.musicbrainz_id == "123"


def test_can_list(repo, setup_artists):
    artists = repo.list()
    assert len(artists) == 2
    assert type(artists[0]) == Artist
    assert artists[0].name == "The Fake Artist"


def test_can_get(repo, setup_artists):
    artist = repo.get(id=2)
    assert artist.name == "The 2nd Fake Artist"


def test_can_update(repo, setup_artists):
    repo.update(id=1, musicbrainz_id="456", name="The New Artist")
    artist = repo.get(id=1)
    assert artist.name == "The New Artist"


def test_can_delete(repo, setup_artists):
    repo.delete(id=1)
    assert len(repo.list()) == 1


def test_raises_not_found(repo, setup_artists):
    with pytest.raises(NotFoundError):
        repo.get(3)


def test_raises_already_exists(repo, setup_artists):
    with pytest.raises(AlreadyExistsError):
        repo.create(musicbrainz_id="456")
