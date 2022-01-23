from deckman.model.artist import Artist

def add_artist_by_musicbrainz_id(musicbrainz_id: str, mb, repo, session):
    info = mb.get_artist_info(musicbrainz_id)
    artist = Artist("123", info.name, info.name_sort)
    repo.add(artist)
    session.commit()
