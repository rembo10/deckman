from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from functools import reduce
from typing import List, Optional

from deckman.model.info_service import InfoService
from deckman.model.profile import Profile


class ARTIST_STATUS(Enum):
    TRACKING = "tracking"
    PAUSED = "paused"
    IGNORED = "ignored"


@dataclass
class Artist:
    id: int
    musicbrainz_id: str
    name: Optional[str] = None
    name_sort: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None
    profile: Optional[Profile] = None
    status: ARTIST_STATUS = ARTIST_STATUS.TRACKING
    updated: Optional[datetime] = None

    def update_info(self, info_service: InfoService):
        info = info_service.get_artist_info(self.musicbrainz_id)
        self.name = info.name
        self.name_sort = info.name_sort
        self.image_url = info.image_url
        self.description = info.description
        self.updated = datetime.now()


class JoinArtist(Artist):
    """Represents an artist how it might appear on a track or album,
    e.g. XXX & YYY -> artist_name = XXX, join_phrase = " & ", or:
    XXX feat. YYY and ZZZ -> artist_name = YYY, join_phrase = " and "
    """
    def __init__(self, artist: Artist, join_phrase: str, position: int):
        self.artist = artist
        self.join_phrase = join_phrase
        self.position = position


def join(jas: List[JoinArtist]) -> Optional[str]:
    def func(a, b):
        if a is None or b.artist.name is None:
            return None
        else:
            return a + b.artist.name + b.join_phrase
    return reduce(
        func,
        sorted(jas, key=lambda x: x.position),
        ""
    )


class ArtistRepo(ABC):

    @abstractmethod
    def add(self, artist: Artist):
        raise NotImplementedError

    @abstractmethod
    def get(self, id: int):
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Artist]:
        raise NotImplementedError
