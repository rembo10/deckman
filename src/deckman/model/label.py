from abc import ABC
from dataclasses import dataclass
from typing import List, Optional


@dataclass
class LabelInfo:
    name: str
    name_sort: str
    image_url: Optional[str] = None
    description: Optional[str] = None


@dataclass
class ExternalLabel:

    id: str

    def get_info(self) -> LabelInfo:
        raise NotImplementedError


class Label:
    def __init__(
        self,
        external: ExternalLabel,
        info: LabelInfo = None,
        tracking: bool = True
    ):
        self.external = external
        self.info = info
        self.tracking = tracking

    def update_info(self):
        self.info = self.external.get_info()


class LabelRepo(ABC):

    def add(self, label: Label):
        raise NotImplementedError

    def get(self) -> List[Label]:
        raise NotImplementedError
