#!/usr/bin/env python

import json

from sqlalchemy import create_engine
import uvicorn

from deckman.api import create_app
from deckman.database.repos import SQLAlchemySettingsLossyRepo
from deckman.database.tables import metadata_obj, settings_lossy


def start():
    engine = create_engine("sqlite+pysqlite:///deckman.db", future=True)
    metadata_obj.create_all(engine)
    with engine.connect() as conn:
        with open("src/deckman/database/initial/settings_lossy.json") as f:
            data = json.load(f)
            try:
                conn.execute(settings_lossy.insert(), data)
                conn.commit()
            except:
                pass
    repo = SQLAlchemySettingsLossyRepo(engine)
    app = create_app(repo)
    uvicorn.run(app)


if __name__ == "__main__":
    start()
