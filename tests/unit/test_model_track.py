from typing import List

from deckman.model.album import Album, AlbumInfo, ExternalAlbum
from deckman.model.track import ExternalTrack, Track, TrackInfo, TrackRepo

from .utils import make_join_artists


class FakeTrackRepo(TrackRepo):

    def __init__(self, tracks: List[Track] = []):
        self.tracks = tracks

    def add(self, track: Track):
        self.tracks.append(track)

    def get(self) -> List[Track]:
        return self.tracks


class FakeExternalTrack(ExternalTrack):
    def get_info(self) -> TrackInfo:
        return TrackInfo(
            "Fake Track",
            make_join_artists([" & ", " feat. ", ""]),
            [
                Album(
                    ExternalAlbum("1"),
                    AlbumInfo(
                        "FakeAlbum1",
                        make_join_artists([" & ", ""])
                    )
                )
            ]
        )


def test_can_add_track():
    track = Track(FakeExternalTrack("1"))
    repo = FakeTrackRepo()
    repo.add(track)
    assert repo.get() == [track]
