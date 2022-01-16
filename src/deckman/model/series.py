from abc import ABC
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class SeriesInfo:
    name: str
    name_sort: str
    image_url: Optional[str] = None
    description: Optional[str] = None


@dataclass
class ExternalSeries:

    id: str

    def get_info(self) -> SeriesInfo:
        raise NotImplementedError


class Series:
    def __init__(
        self,
        external: ExternalSeries,
        info: SeriesInfo = None,
        tracking: bool = True
    ):
        self.external = external
        self.info = info
        self.tracking = tracking

    def update_info(self):
        self.info = self.external.get_info()


class SeriesRepo(ABC):

    def add(self, series: Series):
        raise NotImplementedError

    def get(self) -> List[Series]:
        raise NotImplementedError
