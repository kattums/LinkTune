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
        album = track['album']['name']

        return {'artist': artists[0], 'title': title, 'album': album}

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

    def get_service_url(self, info):
        # remove extra characters present in track title
        title = re.sub("\(.*?\)|\[.*?\]","",info['title']).rstrip()

        # TODO: find less hacky way of solving artists being returned as a list by some platforms and include extra artists in query
        if isinstance(info['artist'], list):
            artist = info['artist'][0]
        else:
            artist = info['artist']

        query = f"{info['title']} artist:{artist}"

        if 'album' in info:
            query += f" album:{info['album']}"
            
        result = self.sp.search(query, limit=1, type='track')

        if result['tracks']['total'] > 0:
            # get top track from results
            top_track = result['tracks']['items'][0]
            track_artist = []
            for artist in top_track['artists']:
                track_artist.append(artist['name'])

            track_title = top_track['name']
            track_url = top_track['external_urls']['spotify']
            return {'service': 'Spotify', 'title': track_title, 'artist': track_artist, 'url': track_url}
        else:
            return f"Could not find track {title} by {artist} on Spotify."