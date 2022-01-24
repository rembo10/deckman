from typing import List

from deckman.model.artist import Artist, ArtistRepo
from deckman.model.info_service import ArtistInfo, InfoService


class FakeArtistRepo(ArtistRepo):
    def __init__(self, artists: List[Artist] = None):
        self.artists = artists or []

    def add(self, artist: Artist):
        self.artists.append(artist)

    def get(self, id: int) -> Artist:
        return next(x for x in self.artists if x.id == id)

    def list(self) -> List[Artist]:
        return self.artists


class FakeInfoService(InfoService):
    def get_artist_info(self, id: str) -> ArtistInfo:
        return ArtistInfo(
                "The Fake Artist", "Fake Artist, The")
