from deckman.services import (
    add_artist_by_musicbrainz_id
)

from .shared import FakeArtistRepo, FakeInfoService


class FakeSession:
    commited = False

    def commit(self):
        self.commited = True


def test_can_add_artist_by_musicbrainz_id():
    info_service = FakeInfoService()
    repo = FakeArtistRepo()
    session = FakeSession()
    print(repo.artists)
    add_artist_by_musicbrainz_id("123", info_service, repo, session)
    print(repo.artists)
    assert len(repo.artists) == 1
    assert repo.artists[0].name == "The Fake Artist"
    assert session.commited is True
