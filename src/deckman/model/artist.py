from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from functools import reduce
from typing import List, Optional


class ArtistStatus(Enum):
    TRACKING = "tracking"
    PAUSED = "paused"
    IGNORED = "ignored"


@dataclass(frozen=True)
class Artist:
    id: int
    musicbrainz_id: str
    name: Optional[str] = None
    name_sort: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None
#    profile: Optional[Profile] = None
    status: ArtistStatus = ArtistStatus.TRACKING
#    updated_at: Optional[datetime] = None


@dataclass(frozen=True)
class JoinArtist:
    """Represents an artist how it might appear on a track or album,
    e.g. XXX & YYY -> artist_name = XXX, join_phrase = " & ", or:
    XXX feat. YYY and ZZZ -> artist_name = YYY, join_phrase = " and "
    """
    artist: Artist
    join_phrase: str
    position: int


class ArtistRepo(ABC):

    @abstractmethod
    def create(self, musicbrainz_id: str) -> Artist:
        raise NotImplementedError

    @abstractmethod
    def get(self, id: int) -> Artist:
        raise NotImplementedError

    @abstractmethod
    def list(self) -> List[Artist]:
        raise NotImplementedError


def join(jas: List[JoinArtist]) -> Optional[str]:
    def f(a, b):
        if a is None or b.artist.name is None:
            return None
        else:
            return a + b.artist.name + b.join_phrase
    return reduce(
        f,
        sorted(jas, key=lambda x: x.position),
        ""
    )
