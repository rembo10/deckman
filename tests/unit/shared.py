from typing import List

from deckman.model.artist import Artist, ArtistRepo


class FakeArtistRepo(ArtistRepo):
    def __init__(self, artists: List[Artist] = []):
        self.artists = artists

    def add(self, artist: Artist):
        artist.id = len(self.artists) + 1 
        self.artists.append(artist)

    def get(self, id: int) -> Artist:
        return next(x for x in self.artists if x.id == id) 

    def list(self) -> List[Artist]:
        return self.artists
