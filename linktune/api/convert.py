from linktune.api.tidal import Tidal
from linktune.api.spotify import Spotify
from linktune.api.deezer import Deezer
from linktune.api.applemusic import AppleMusic
from linktune.api.youtube import YouTube
from linktune.config.config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET

class Convert:
    def __init__(self):
        self.spotify = Spotify(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
        self.tidal = Tidal()
        self.deezer = Deezer()
        self.apple = AppleMusic()
        self.youtube = YouTube()

    def convert_link(self, link, target_service):
        if "spotify" in link:
            source_service = self.spotify
        elif "tidal" in link:
            source_service = self.tidal
        elif "deezer" in link:
            source_service = self.deezer
        elif 'apple' in link:
            source_service = self.apple
        elif 'youtube' in link:
            source_service = self.youtube
        else:
            return None

        track_info = source_service.get_track_info(link)

        if not track_info:
            return None

# TODO: clean up this repetitive crap
        if target_service == 'spotify':
            return self.spotify.get_url(track_info)
        elif target_service == 'tidal':
            return self.tidal.get_url(track_info)
        elif target_service == 'apple':
            return self.apple.get_url(track_info)
        elif target_service == 'youtube':
            return self.youtube.get_url(track_info)
        else:
            return "Something went wrong."