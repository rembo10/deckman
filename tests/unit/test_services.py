from typing import List

from deckman.model.artist import Artist, ArtistInfo, ArtistRepo
from deckman.services import (
    add_artist_by_musicbrainz_id
)

from .shared import FakeArtistRepo

class FakeSession:
    commited = False

    def commit(self):
        self.commited = True

class FakeMusicBrainz:
    def get_artist_info(self, musicbrainz_id: str) -> ArtistInfo:
        return ArtistInfo(
                "The Fake Artist", "Fake Artist, The")

def test_can_add_artist_by_musicbrainz_id():
    mb = FakeMusicBrainz()
    repo = FakeArtistRepo()
    session = FakeSession()
    add_artist_by_musicbrainz_id("123", mb, repo, session)  
    assert len(repo.artists) == 1
    assert repo.artists[0].name == "The Fake Artist"
    assert session.commited == True

