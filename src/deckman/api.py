# from typing import List, Optional
#
# from fastapi import FastAPI
# from pydantic import BaseModel
#
# from deckman.model.artist import ArtistRepo
#
#
# class Artist(BaseModel):
#     id: Optional[int]
#     name: str
#     name_sort: str
#
#
# def API(repo: ArtistRepo):
#
#     app = FastAPI()
#
#     @app.get("/artists/", response_model=List[Artist])
#     def read_artists():
#         artists = repo.get()
#         artists = map(
#             lambda x: {
#                     "id": x.id,
#                     "name": x.info.name,
#                     "name_sort": x.info.name_sort
#                 }, artists)
#         return [Artist(**a) for a in artists]
#
#     return app
