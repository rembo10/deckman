# from fastapi.testclient import TestClient

# from deckman.api import API
# from deckman.model.artist import Artist, ArtistRepo


# def test_read_artists():
#     app = API(FakeArtistRepo())
#     client = TestClient(app)
#     response = client.get("/artists")
#     assert response.status_code == 200
#     assert response.json() == [
#             {
#                 "id": 1,
#                 "name": "The Fake Artist",
#                 "name_sort": "Fake Artist, The",
#             }
#         ]
