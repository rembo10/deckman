from typing import List, Optional

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from sqlalchemy.engine import Engine

from deckman.database.repos import (
    SQLAlchemyBaseRepo,
    SQLAlchemySettingsLosslessRepo,
    SQLAlchemySettingsLossyRepo,
    SQLAlchemyProfileRepo,
    SQLAlchemyQualityRepo
    )


class SettingsLossyPost(BaseModel):
    name: str
    bitrate: int


class SettingsLosslessPost(BaseModel):
    name: str
    sample_rate_hz: int
    bit_depth: int
    channels: int

class ProfilePost(BaseModel):
    name: str
    position: int

class QualityPost(BaseModel):
    profile_id: int
    position: int
    settings_lossy_id: Optional[int]
    settings_lossless_id: Optional[int]
    finish: bool


def make_generic_routes(
    app: FastAPI,
    engine: Engine,
    endpoint: str,
    Repo: SQLAlchemyBaseRepo,
    Model: BaseModel,
    bulk: bool = False
):

    @app.get(f"/api/{endpoint}")
    def get():
        with engine.connect() as conn:
            repo = Repo(conn)
            return repo.list()

    @app.post(f"/api/{endpoint}", status_code=201)
    def post(params: Model):
        with engine.connect() as conn:
            repo = Repo(conn)
            result = repo.create(**params.dict())
            conn.commit()
        return result

    @app.put(f"/api/{endpoint}/{{id}}")
    def put(id: int, params: Model):
        with engine.connect() as conn:
            repo = Repo(conn)
            repo.update(id=id, **params.dict())
            conn.commit()

    @app.delete(f"/api/{endpoint}/{{id}}")
    def delete(id: int):
        with engine.connect() as conn:
            repo = Repo(conn)
            repo.delete(id=id)
            conn.commit()

    if bulk:
        @app.put(f"/api/{endpoint}")
        def put(params: List[Model]):
            pass


def create_app(engine: Engine):

    app = FastAPI()

    routes = [
        {
            "endpoint": "settings-lossy",
            "Repo": SQLAlchemySettingsLossyRepo,
            "Model": SettingsLossyPost
        },
        {
            "endpoint": "settings-lossless",
            "Repo": SQLAlchemySettingsLosslessRepo,
            "Model": SettingsLosslessPost
        },
        {
            "endpoint": "profiles",
            "Repo": SQLAlchemyProfileRepo,
            "Model": ProfilePost,
            "bulk": True
        },
        {
            "endpoint": "qualities",
            "Repo": SQLAlchemyQualityRepo,
            "Model": QualityPost,
            "bulk": True
        }
    ]

    for route in routes:
        make_generic_routes(app, engine, **route)

    app.mount("/dist/", StaticFiles(directory="dist"))

    return app
