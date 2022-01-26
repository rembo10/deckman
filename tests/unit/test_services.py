from deckman.model.events import (
    ArtistAdded,
    Event
)

from deckman.model.services import (
    add_artist_by_musicbrainz_id
)

from .shared import FakeArtistRepo


class FakeDBConnection:
    commited = False

    def commit(self):
        self.commited = True


class FakeBus:

    def __init__(self):
        self.events = []

    def push(self, event: Event):
        self.events.append(event)


def test_can_add_artist_by_musicbrainz_id():
    db = FakeDBConnection()
    repo = FakeArtistRepo()
    bus = FakeBus()
    add_artist_by_musicbrainz_id(
        repo=repo,
        db=db,
        bus=bus,
        musicbrainz_id="123")
    assert len(repo.artists) == 1
    assert len(bus.events) == 1
    assert type(bus.events[0]) == ArtistAdded
    assert bus.events[0].artist.id == 1
    assert db.commited is True
