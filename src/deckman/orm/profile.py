from sqlalchemy import (
    Boolean,
    CheckConstraint,
    Column,
    Float,
    ForeignKey,
    Integer,
    MetaData,
    String,
    Table,
    UniqueConstraint,
)


metadata_obj = MetaData()


settings_lossless = Table(
    "settings_lossless",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(128), unique=True),
    Column("sample_rate_khz", Float),
    Column("bit_depth", Integer),
    Column("channels", Integer),
    UniqueConstraint("sample_rate_khz", "bit_depth", "channels")
)


settings_lossy = Table(
    "settings_lossy",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(128), unique=True),
    Column("bitrate", Integer, unique=True)
)


qualities = Table(
    "qualities",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("finish", Boolean),
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
    Column("profile_id", ForeignKey("profiles.id")),
    Column("position", Integer),
    CheckConstraint(
        "(settings_lossy_id IS NULL) <> (settings_lossless_id IS NULL)",
        name="lossy_xor_lossless"
    )
)


profiles = Table(
    "profiles",
    metadata_obj,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("name", String(128), unique=True),
    Column("tolerance", Float, default=0.2),
    Column("dual_formats", Boolean, default=False),
)
