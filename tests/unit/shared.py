from typing import List

from deckman.model.artist import Artist, ArtistRepo


class FakeArtistRepo(ArtistRepo):
    def __init__(self, artists: List[Artist] = None):
        self.artists = artists or []

    def create(self, musicbrainz_id: str) -> Artist:
        id = len(self.artists) + 1
        artist = Artist(id=id, musicbrainz_id=musicbrainz_id)
        self.artists.append(artist)
        return artist

    def get(self, id: int) -> Artist:
        return next(x for x in self.artists if x.id == id)

    def list(self) -> List[Artist]:
        return self.artists
