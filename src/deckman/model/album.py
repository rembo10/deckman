from abc import ABC
from dataclasses import dataclass
from datetime import date
from typing import List, Optional

from deckman.model.artist import JoinArtist
from deckman.model.profile import Profile


@dataclass
class AlbumInfo:
    title: str
    title_sort: str
    artists: List[JoinArtist]
    release_date: Optional[date]
    image_url: Optional[str]
    description: Optional[str]


@dataclass
class ExternalAlbum:

    id: str

    def get_info(self) -> AlbumInfo:
        raise NotImplementedError


class Album:

    def __init__(
        self,
        external: ExternalAlbum,
        info: AlbumInfo,
        wanted_profile: Profile = None
    ):
        self.external = external
        self.info = info
        self.wanted_profile = wanted_profile


class AlbumRepo(ABC):

    def add(self, album: Album):
        raise NotImplementedError

    def get(self) -> List[Album]:
        raise NotImplementedError
