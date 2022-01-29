#!/usr/bin/env python

import json

from sqlalchemy import create_engine
import uvicorn

from deckman.api import create_app
from deckman.database.repos import SQLAlchemySettingsLossyRepo
from deckman.database.tables import *


def start():
    engine = create_engine("sqlite+pysqlite:///deckman.db", future=True)
    metadata_obj.create_all(engine)
    with engine.connect() as conn:
        for file, table in [
            ("settings_lossy", settings_lossy),
            ("settings_lossless", settings_lossless),
            ("qualities", qualities),
            ("profiles", profiles)
        ]:

            with open(f"src/deckman/database/initial/{file}.json") as f:
                data = json.load(f)
                try:
                    conn.execute(table.insert(), data)
                    conn.commit()
                except Exception as e:
                    pass
    app = create_app(engine)
    uvicorn.run(app, port=8181)


if __name__ == "__main__":
    start()
