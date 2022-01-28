from typing import List, Optional

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from deckman.model.profile import SettingsLossyRepo


class SettingsLossyPost(BaseModel):
    name: str
    bitrate: int

def create_app(repo: SettingsLossyRepo):

    app = FastAPI()

    @app.get("/api/settings-lossy/")
    def get_settings_lossy():
        return repo.list()

    @app.post("/api/settings-lossy/")
    def post_settings_lossy(params: SettingsLossyPost):
        return repo.create(**params.dict())

    @app.put("/api/settings-lossy/{id}")
    def put_settings_lossy(id: int, params: SettingsLossyPost):
        return repo.update(id=id, **params.dict())

    @app.delete("/api/settings-lossy/{id}")
    def delete_settings_lossy(id: int):
        repo.delete(id=id)


    app.mount("/", StaticFiles(directory="dist"), name="dist")

    return app
