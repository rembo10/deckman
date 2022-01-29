from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Enum,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    UniqueConstraint,
)

from deckman.model.artist import ArtistStatus


metadata_obj = MetaData()


artists = Table(
    "artists",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("musicbrainz_id", String(36), unique=True),
    Column("name", String(512), nullable=True),
    Column("name_sort", String(512), nullable=True),
    Column("image_url", String(512), nullable=True),
    Column("description", String(2048), nullable=True),
    Column("status", Enum(ArtistStatus, create_constraint=True)),
    # Column("profile_id", ForeignKey("profile.id"), nullable=True),
)


settings_lossless = Table(
    "settings_lossless",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(128), unique=True),
    Column("sample_rate_hz", Integer),
    Column("bit_depth", Integer),
    Column("channels", Integer),
    UniqueConstraint("sample_rate_hz", "bit_depth", "channels")
)


settings_lossy = Table(
    "settings_lossy",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(128), unique=True),
    Column("bitrate", Integer, unique=True)
)


qualities = Table(
    "qualities",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("profile_id", ForeignKey("profiles.id")),
    Column("position", Integer),
    Column(
        "settings_lossless_id",
        ForeignKey("settings_lossless.id"),
        nullable=True
    ),
    Column(
        "settings_lossy_id",
        ForeignKey("settings_lossy.id"),
        nullable=True
    ),
    Column("finish", Boolean),
    CheckConstraint(
        "(settings_lossy_id IS NULL) <> (settings_lossless_id IS NULL)",
        name="lossy_xor_lossless"
    )
)


profiles = Table(
    "profiles",
    metadata_obj,
    Column("id", Integer, primary_key=True),
    Column("name", String(128), unique=True),
    Column("position", Integer),
    Column("enabled", Boolean, default=True),
    Column("tolerance", Float, default=0.2),
    Column("dual_formats", Boolean, default=False),
)
