from dataclasses import dataclass

from deckman.model.artist import Artist


class Event:
    pass


@dataclass(frozen=True)
class ArtistAdded(Event):
    artist: Artist
