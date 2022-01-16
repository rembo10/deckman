from abc import ABC
from dataclasses import dataclass
from enum import Enum
from typing import List, Optional


class ARTIST_STATUS(Enum):
    TRACKING = "tracking"
    PAUSED = "paused"
    IGNORED = "ignored"


@dataclass
class ArtistInfo:
    name: str
    name_sort: str
    image_url: Optional[str] = None
    description: Optional[str] = None


@dataclass
class ExternalArtist:

    id: str

    def get_info(self) -> ArtistInfo:
        raise NotImplementedError


class Artist:
    def __init__(
        self,
        external: ExternalArtist,
        info: ArtistInfo = None,
        status: ARTIST_STATUS = ARTIST_STATUS.TRACKING

    ):
        self.external = external
        self.info = info
        self.status = status

    def update_info(self):
        self.info = self.external.get_info()


class JoinArtist(Artist):
    """Represents an artist how it might appear on a track or album,
    e.g. XXX & YYY -> artist_name = XXX, join_phrase = " & ", or:
    XXX feat. YYY and ZZZ -> artist_name = YYY, join_phrase = " and "
    """
    def __init__(self, artist: Artist, join_phrase: str, position: int):
        self.artist = artist
        self.join_phrase = join_phrase
        self.position = position


class ArtistRepo(ABC):

    def add(self, artist: Artist):
        raise NotImplementedError

    def get(self) -> List[Artist]:
        raise NotImplementedError
