from abc import ABC
from dataclasses import dataclass
from datetime import date
from typing import List, Optional

from deckman.model.artist import JoinArtist
from deckman.model.profile import Profile


@dataclass
class AlbumInfo:
    title: str
    artists: List[JoinArtist]
    release_date: Optional[date] = None
    image_url: Optional[str] = None
    description: Optional[str] = None


@dataclass
class ExternalAlbum:

    id: str

    def get_info(self) -> AlbumInfo:
        raise NotImplementedError


class Album:

    def __init__(
        self,
        external: ExternalAlbum,
        info: Optional[AlbumInfo] = None,
        wanted_profile: Optional[Profile] = None
    ):
        self.external = external
        if info is None:
            self.update_info()
        else:
            self.info = info
        self.wanted_profile = wanted_profile

    def update_info(self):
        self.info = self.external.get_info()


class AlbumRepo(ABC):

    def add(self, album: Album):
        raise NotImplementedError

    def get(self) -> List[Album]:
        raise NotImplementedError
