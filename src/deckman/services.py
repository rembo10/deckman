from deckman.model.artist import Artist


def add_artist_by_musicbrainz_id(
    musicbrainz_id: str,
    info_service,
    repo,
    session
):

    info = info_service.get_artist_info(musicbrainz_id)
    artist = Artist(1, musicbrainz_id, info.name, info.name_sort)
    repo.add(artist)
    session.commit()
