from abc import ABC, abstractmethod


class InfoService(ABC):

    @abstractmethod
    def get_artist_info(self, id: str) -> None:
        raise NotImplementedError
