import spotipy
import re
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.cache_handler import MemoryCacheHandler

class Spotify:
    def __init__(self, client_id, client_secret):
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret, cache_handler=MemoryCacheHandler()))

    def get_track_info(self, track_url):
        print('Searching for track...')
        track_id = self._get_track_id(track_url)
        if not track_id:
            return 'Could not identify Spotify track ID'

        track = self.sp.track(track_id)
        artists = [artist['name'] for artist in track['artists']]
        title = track['name']

        return {'artist': artists, 'title': title}

    def _get_track_id(self, track_url):
        track_id = None
        # check if Spotify internal id is appended to the link and remove if so
        if '?si=' in track_url:
            track_url = track_url.split('?si=')[0]
        if 'open.spotify.com/track/' in track_url:
            _, _, track_id = track_url.rpartition('/')
        elif 'spotify:track:' in track_url:
            _, _, track_id = track_url.rpartition(':')

        return track_id

    def get_url(self, info):
        title = info['title']
        # remove extra characters present in track title
        title = re.sub("\(.*?\)|\[.*?\]","",title).rstrip()

        artist = info['artist']
        query = f"{title} artist:{artist}"

        result = self.sp.search(query, limit=1, type='track')

        if result['tracks']['total'] > 0:
            uri = result['tracks']['items'][0]['uri']
            _, _, track_id = uri.rpartition(':')
            return f"info: {title} by {artist}, url: open.spotify.com/track/{track_id}"
        else:
            return 'Track not found.'