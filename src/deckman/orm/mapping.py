from sqlalchemy import (
        Table, Column, Integer, String, ForeignKey, MetaData, Enum)
from sqlalchemy.orm import registry, relationship

from deckman.model.artist import Artist, ArtistInfo, ARTIST_STATUS
from deckman.info.musicbrainz import MusicBrainzArtist

mapper_registry = registry()
metadata_obj = MetaData()

musicbrainz_artist = Table(
    "musicbrainz_artist",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("external_id", String(36)),
)

artist = Table(
    "artist",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("external_id", Integer, ForeignKey("musicbrainz_artist.id")),
    Column("info_id", Integer, ForeignKey("artist_info.id")),
    Column("status", Enum(ARTIST_STATUS, create_constraint=True))
)

artist_info = Table(
    "artist_info",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(512)),
    Column("name_sort", String(512)),
    Column("image_url", String(512)),
    Column("description", String(2048)),
)


def run_mappers():
    mapper_registry.map_imperatively(MusicBrainzArtist, musicbrainz_artist)
    mapper_registry.map_imperatively(ArtistInfo, artist_info)
    mapper_registry.map_imperatively(
        Artist,
        artist,
        properties={
            "external": relationship(MusicBrainzArtist),
            "info": relationship(ArtistInfo)
        }
    )
