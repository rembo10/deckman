from typing import List

from deckman.model.artist import Artist, JoinArtist


def make_join_artist(idx: int, jp: str) -> JoinArtist:
    artist = Artist(
        id=idx + 1,
        musicbrainz_id=str(idx),
        name=f"FA{idx}"
    )
    return JoinArtist(
        artist=artist,
        join_phrase=jp,
        position=idx
    )


def make_join_artists(jps: List[str]) -> List[JoinArtist]:
    return [make_join_artist(idx, jp) for idx, jp in enumerate(jps)]
