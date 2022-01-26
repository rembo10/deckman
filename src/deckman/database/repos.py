from typing import List

from sqlalchemy import insert, select
from sqlalchemy.engine import Connection

from deckman.database.tables import artists  # type: ignore
from deckman.model.artist import Artist, ArtistRepo
from deckman.model.exceptions import NotFoundError


class SQLAlchemyArtistRepo(ArtistRepo):

    def __init__(self, conn: Connection) -> None:
        self.conn = conn

    def create(self, musicbrainz_id: str) -> Artist:
        stmt = insert(artists).values(musicbrainz_id=musicbrainz_id)
        result = self.conn.execute(stmt)
        return Artist(
            id=result.inserted_primary_key[0],
            musicbrainz_id=musicbrainz_id
        )

    def get(self, artist_id: int) -> Artist:
        stmt = select(artists).where(artists.c.id == artist_id)
        cursor = self.conn.execute(stmt)
        row = cursor.fetchone()
        if row:
            return Artist(**row._asdict())
        else:
            raise NotFoundError

    def list(self) -> List[Artist]:
        stmt = select(artists)
        cursor = self.conn.execute(stmt)
        rows = cursor.fetchall()
        return [Artist(**row._asdict()) for row in rows]
