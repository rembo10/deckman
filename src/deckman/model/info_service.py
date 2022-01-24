from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional


@dataclass
class ArtistInfo:
    name: str
    name_sort: Optional[str] = None
    image_url: Optional[str] = None
    description: Optional[str] = None


class InfoService(ABC):

    @abstractmethod
    def get_artist_info(self, id: str) -> ArtistInfo:
        raise NotImplementedError
