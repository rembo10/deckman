import pytest

from deckman.model.artist import (
        Artist,
        join,
    )

from .shared import FakeArtistRepo
from .utils import make_join_artists


@pytest.fixture
def fake_artist():
    return Artist(id=1, musicbrainz_id="f1")


def test_can_create_artist():
    repo = FakeArtistRepo()
    repo.create(musicbrainz_id="123")
    assert repo.artists == [
        Artist(id=1, musicbrainz_id="123")
    ]


def test_can_can_join_artists():
    join_artists = make_join_artists([" & ", ""])
    assert join(join_artists) == "FA0 & FA1"


def test_join_order_doesnt_matter():
    join_artists = make_join_artists([" & ", ""])
    assert join([join_artists[1], join_artists[0]]) == "FA0 & FA1"


def test_join_single_artist():
    join_artists = make_join_artists([""])
    assert join(join_artists) == "FA0"
