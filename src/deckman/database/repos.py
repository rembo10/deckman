from typing import Generic, List, TypeVar

from sqlalchemy import delete, insert, select, update
from sqlalchemy.engine import Connection
from sqlalchemy.exc import IntegrityError

from deckman.database.tables import *  # type: ignore
from deckman.model.artist import Artist, ArtistRepo
from deckman.model.profile import (
    SettingsLossless,
    SettingsLosslessRepo,
    SettingsLossy,
    SettingsLossyRepo,
    Profile,
    ProfileRepo,
    Quality,
    QualityRepo,
    )
from deckman.model.exceptions import AlreadyExistsError, NotFoundError


T = TypeVar('T')

class SQLAlchemyBaseRepo(Generic[T]):

    def __init__(self, connection: Connection) -> None:
        self.connection = connection

    def create(self, **kwargs) -> T:
        stmt = insert(self.table).values(**kwargs)
        try:
            result = self.connection.execute(stmt)
        except IntegrityError:
            raise AlreadyExistsError
        return self.model(id=result.inserted_primary_key[0], **kwargs)

    def get(self, id: int) -> T:
        stmt = select(self.table).where(self.table.c.id == id)
        cursor = self.connection.execute(stmt)
        row = cursor.fetchone()
        if row:
            return self.model(**row._asdict())
        else:
            raise NotFoundError

    def list(self) -> List[T]:
        stmt = select(self.table)
        cursor = self.connection.execute(stmt)
        rows = cursor.fetchall()
        return [self.model(**row._asdict()) for row in rows]

    def update(self, id: int, **kwargs) -> T:
        stmt = update(self.table).where(self.table.c.id == id).values(**kwargs)
        self.connection.execute(stmt)
        return self.model(id=id, **kwargs)

    def delete(self, id: int) -> None:
        stmt = delete(self.table).where(self.table.c.id == id)
        self.connection.execute(stmt)

class SQLAlchemyArtistRepo(SQLAlchemyBaseRepo):
    model = Artist
    table = artists

class SQLAlchemySettingsLossyRepo(SQLAlchemyBaseRepo):
    model = SettingsLossy
    table = settings_lossy

class SQLAlchemySettingsLosslessRepo(SQLAlchemyBaseRepo):
    model = SettingsLossless
    table = settings_lossless

class SQLAlchemyProfileRepo(SQLAlchemyBaseRepo):
    model = Profile
    table = profiles

class SQLAlchemyQualityRepo(SQLAlchemyBaseRepo):
    model = Quality
    table = qualities
