from deckman.model.artist import ArtistInfo, ExternalArtist


class MusicBrainzArtist(ExternalArtist):
    external_id: str

    def get_info(self) -> ArtistInfo:
        return ArtistInfo("Some Artist")
