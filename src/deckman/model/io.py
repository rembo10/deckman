from abc import ABC, abstractmethod
from pathlib import Path


class IO(ABC):

    @abstractmethod
    def move(self, src: Path, dest: Path):
        raise NotImplementedError

    @abstractmethod
    def remove(self, path: Path):
        raise NotImplementedError
