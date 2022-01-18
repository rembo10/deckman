from typing import List

import pytest

from deckman.model.artist import (
        ARTIST_STATUS,
        Artist,
        ArtistInfo,
        ArtistRepo,
        ExternalArtist,
        JoinArtist,
        join
    )


class FakeExternalArtist(ExternalArtist):
    def get_info(self) -> ArtistInfo:
        return ArtistInfo("The Fake Artist")


@pytest.fixture
def fake_artist():
    return Artist(FakeExternalArtist("1"))


class FakeArtistRepo(ArtistRepo):
    def __init__(self, artists: List[Artist] = []):
        self.artists = artists

    def add(self, artist: Artist):
        self.artists.append(artist)

    def get(self) -> List[Artist]:
        return self.artists


def test_can_add_artist(fake_artist):
    repo = FakeArtistRepo()
    repo.add(fake_artist)
    assert repo.get() == [fake_artist]


def test_new_artist_defaults_to_tracking(fake_artist):
    assert fake_artist.status == ARTIST_STATUS.TRACKING


def test_can_get_artist_info(fake_artist):
    fake_artist.update_info()
    assert fake_artist.info.name == "The Fake Artist"


def make_join_artists(jps: List[str]) -> List[JoinArtist]:
    def make_join_artist(idx: int, jp: str) -> JoinArtist:
        return JoinArtist(
            Artist(ExternalArtist(str(idx)), ArtistInfo(f"FA{idx}")),
            jp, idx)
    return [make_join_artist(idx, jp) for idx, jp in enumerate(jps)]


def test_can_can_join_artists():
    join_artists = make_join_artists([" & ", ""])
    assert join(join_artists) == "FA0 & FA1"


def test_join_order_doesnt_matter():
    join_artists = make_join_artists([" & ", ""])
    assert join([join_artists[1], join_artists[0]]) == "FA0 & FA1"


def test_join_single_artist():
    join_artists = make_join_artists([""])
    assert join(join_artists) == "FA0"
