from deckman.model.events import ArtistAdded


def add_artist_by_musicbrainz_id(
    repo,
    db,
    bus,
    musicbrainz_id: str,
):
    artist = repo.create(musicbrainz_id=musicbrainz_id)
    db.commit()
    bus.push(event=ArtistAdded(artist=artist))
