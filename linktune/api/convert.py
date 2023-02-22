from linktune.api.tidal import Tidal
from linktune.api.spotify import Spotify
from linktune.config.config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET

class Convert:
    def __init__(self):
        self.spotify = Spotify(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
        self.tidal = Tidal()

    def convert_link(self, link, target_service):
        if "spotify" in link:
            source_service = self.spotify
        elif "tidal" in link:
            source_service = self.tidal
        else:
            return None

        track_info = source_service.get_track_info(link)

        if not track_info:
            return None

        if target_service == 'spotify':
            return self.spotify.get_url(track_info)
        elif target_service == 'tidal':
            return self.tidal.get_url(track_info)
        else:
            return "Something went wrong."