from abc import ABC
from dataclasses import dataclass
from typing import List

from deckman.model.artist import JoinArtist
from deckman.model.album import Album
from deckman.model.profile import Profile


@dataclass
class TrackInfo:
    title: str
    artists: List[JoinArtist]
    albums: List[Album]


@dataclass
class ExternalTrack:
    """An external entity used to specifically identify a track.
    It's the class that's used also to fetch information.
    """
    id: str

    def get_info(self) -> TrackInfo:
        raise NotImplementedError


class Track:
    """An internal representation of a track (a particular recording
    that could appear on a number of different albums). It is akin to
    the recording entity on musicbrainz.org.

    It is linked to an external entity (e.g. a musicbrainz recording),
    so we know what exactly it refers to.

    Track numbers, duration, etc. are specific to the album it
    appears on so are not included in the Track class, but rather
    the ReleaseTrack class.
    """
    def __init__(
        self,
        external: ExternalTrack,
        info: TrackInfo,
        wanted_profile: Profile = None
    ):
        self.external = external
        self.info = info
        self.wanted_profile = wanted_profile

    def update_info(self):
        self.info = self.external.get_info()


@dataclass
class ReleaseTrack(Track):
    pass


class TrackRepo(ABC):

    def add(self, track: Track):
        raise NotImplementedError

    def get(self) -> List[Track]:
        raise NotImplementedError
