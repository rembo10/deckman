from typing import List

import pytest

from deckman.model.artist import (
        ARTIST_STATUS,
        Artist,
        ArtistInfo,
        ArtistRepo,
        ExternalArtist,
    )


class FakeArtistRepo(ArtistRepo):
    def __init__(self, artists: List[Artist] = []):
        self.artists = artists

    def add(self, artist: Artist):
        self.artists.append(artist)

    def get(self) -> List[Artist]:
        return self.artists


class FakeExternalArtist(ExternalArtist):
    def get_info(self) -> ArtistInfo:
        return ArtistInfo("The Fake Artist", "Fake Artist, The")


@pytest.fixture
def fake_artist():
    return Artist(FakeExternalArtist("12345"))


def test_can_add_artist(fake_artist):
    repo = FakeArtistRepo()
    repo.add(fake_artist)
    assert repo.get() == [fake_artist]


def test_new_artist_defaults_to_tracking(fake_artist):
    assert fake_artist.status == ARTIST_STATUS.TRACKING


def test_can_get_artist_info(fake_artist):
    fake_artist.update_info()
    assert fake_artist.info.name == "The Fake Artist"
    assert fake_artist.info.name_sort == "Fake Artist, The"
