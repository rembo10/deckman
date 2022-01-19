from typing import List

from sqlalchemy.orm import Session

from deckman.model.artist import Artist, ArtistRepo


class SQLAlchemyArtistRepo(ArtistRepo):
    def __init__(self, session: Session):
        self.session = session

    def add(self, artist: Artist):
        self.session.add(artist)

    def get(self) -> List[Artist]:
        return self.session.query(Artist).all()
