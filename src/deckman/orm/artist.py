from typing import List, Optional

from sqlalchemy import (
    Column,
    Enum,
    Integer,
    MetaData,
    String,
    Table,
)
from sqlalchemy.orm import Session

from deckman.model.artist import Artist, ArtistRepo, ARTIST_STATUS


metadata_obj = MetaData()


artists = Table(
    "artists",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("musicbrainz_id", String(36), unique=True),
    Column("name", String(512), nullable=True),
    Column("name_sort", String(512), nullable=True),
    Column("image_url", String(512), nullable=True),
    Column("description", String(2048), nullable=True),
    Column("status", Enum(ARTIST_STATUS, create_constraint=True)),
    # Column("profile_id", ForeignKey("profile.id"), nullable=True),
)


class SQLAlchemyArtistRepo(ArtistRepo):

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(self, artist: Artist):
        query = artists.insert().values(
            musicbrainz_id=artist.musicbrainz_id,
            name=artist.name,
            name_sort=artist.name_sort,
            image_url=artist.image_url,
            description=artist.description,
            status=artist.status
        )
        self.session.execute(query)

    def get(self, artist_id: int) -> Optional[Artist]:
        query = artists.select().where(artists.c.id == artist_id)
        cursor = self.session.execute(query)
        row = cursor.fetchone()
        if row:
            return Artist(**row._asdict())
        else:
            return None

    def list(self) -> List[Artist]:
        query = artists.select()
        cursor = self.session.execute(query)
        rows = cursor.fetchall()
        return [Artist(**row._asdict()) for row in rows]
