import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from deckman.info.musicbrainz import MusicBrainzArtist
from deckman.model.artist import Artist, ArtistInfo
from deckman.orm.mapping import run_mappers, metadata_obj
from deckman.orm.repos import SQLAlchemyArtistRepo


engine = create_engine("sqlite:///:memory:")
run_mappers()
metadata_obj.create_all(engine)


@pytest.fixture
def session():
    yield Session(engine)


def test_artist_repo_can_save(session):
    artist = Artist(MusicBrainzArtist("1"), ArtistInfo("The Fake Artist"))
    repo = SQLAlchemyArtistRepo(session)
    repo.add(artist)
    session.commit()

    artist_rows = session.execute(
            "SELECT info_id, external_id, status FROM 'artist'")
    assert list(artist_rows) == [(1, 1, "TRACKING")]

    info_rows = session.execute("SELECT name FROM 'artist_info'")
    assert list(info_rows) == [("The Fake Artist",)]

    mb_rows = session.execute("SELECT external_id FROM 'musicbrainz_artist'")
    assert list(mb_rows) == [("1",)]


def test_artist_repo_can_get(session):
    repo = SQLAlchemyArtistRepo(session)
    artists = repo.get()
    assert type(artists[0]) == Artist
    assert artists[0].info.name == "The Fake Artist"
