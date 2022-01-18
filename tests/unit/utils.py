from typing import List

from deckman.model.artist import Artist, ArtistInfo, ExternalArtist, JoinArtist


def make_join_artist(idx: int, jp: str) -> JoinArtist:
    return JoinArtist(
        Artist(ExternalArtist(str(idx)), ArtistInfo(f"FA{idx}")),
        jp, idx)


def make_join_artists(jps: List[str]) -> List[JoinArtist]:
    return [make_join_artist(idx, jp) for idx, jp in enumerate(jps)]
