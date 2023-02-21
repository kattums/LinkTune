from linktune.api.tidal import Tidal
from linktune.api.spotify import Spotify
import os

client_id = os.environ.get('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')

class Convert:
    def __init__(self):
        self.spotify = Spotify(client_id, client_secret)
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


# ConvertObject = Convert()

# print(ConvertObject.convert_link('https://tidal.com/browse/track/24696095', 'spotify'))