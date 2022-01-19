from typing import List

from deckman.model.album import (
        Album, AlbumInfo, ExternalAlbum, AlbumRepo)

from .utils import make_join_artists


class FakeAlbumRepo(AlbumRepo):

    def __init__(self, albums: List[Album] = []):
        self.albums = albums

    def add(self, album: Album):
        self.albums.append(album)

    def get(self) -> List[Album]:
        return self.albums


class FakeExternalAlbum(ExternalAlbum):
    def get_info(self) -> AlbumInfo:
        return AlbumInfo(
            "Fake Album",
            make_join_artists([" & ", ""]),
        )


def test_can_add_album():
    album = Album(FakeExternalAlbum("1"))
    repo = FakeAlbumRepo()
    repo.add(album)
    assert repo.get() == [album]
