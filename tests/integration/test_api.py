
import pytest
from fastapi.testclient import TestClient

from deckman.api import create_app

@pytest.fixture(scope="session")
def client(create_tables):
    engine = create_tables
    app = create_app(engine)
    return TestClient(app)

def test_settings_lossy(client):
    response = client.post(
        "/api/settings-lossy",
        json={"name": "1", "bitrate": 123}
    )
    assert response.status_code == 201

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
