import pytest

from deckman.model.artist import (
        Artist,
        ARTIST_STATUS,
        join
    )

from .shared import FakeArtistRepo, FakeInfoService
from .utils import make_join_artists


@pytest.fixture
def fake_artist():
    return Artist(
            id=1,
            musicbrainz_id="111")


def test_can_update_artist_info(fake_artist):
    fake_artist.update_info(FakeInfoService())
    assert fake_artist.name == "The Fake Artist"
    assert fake_artist.name_sort == "Fake Artist, The"


def test_can_add_artist(fake_artist):
    repo = FakeArtistRepo()
    repo.add(fake_artist)
    assert repo.list() == [fake_artist]


def test_new_artist_defaults_to_tracking(fake_artist):
    assert fake_artist.status == ARTIST_STATUS.TRACKING


def test_can_can_join_artists():
    join_artists = make_join_artists([" & ", ""])
    assert join(join_artists) == "FA0 & FA1"


def test_join_order_doesnt_matter():
    join_artists = make_join_artists([" & ", ""])
    assert join([join_artists[1], join_artists[0]]) == "FA0 & FA1"


def test_join_single_artist():
    join_artists = make_join_artists([""])
    assert join(join_artists) == "FA0"
