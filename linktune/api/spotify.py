import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class Spotify:
    def __init__(self, client_id, client_secret):
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

    def get_track_info(self, track_url):
        track_id = self._get_track_id(track_url)
        if not track_id:
            return None

        track = self.sp.track(track_id)
        artists = [artist['name'] for artist in track['artists']]
        title = track['name']

        return {'artist': artists, 'title': title}

    def _get_track_id(self, track_url):
        track_id = None
        if 'open.spotify.com/track/' in track_url:
            _, _, track_id = track_url.rpartition('/')
        elif 'spotify:track:' in track_url:
            _, _, track_id = track_url.rpartition(':')

        return track_id

    def get_url(self, info):
        title = info['title']
        artist = info['artist']
        query = f"{title} artist:{artist}"

        result = self.sp.search(query, limit=1, type='track')

        if result['tracks']['total'] > 0:
            uri = result['tracks']['items'][0]['uri']
            _, _, track_id = uri.rpartition(':')
            return f'open.spotify.com/track/{track_id}'
        else:
            print('Track not found.')

# # testing that it works
# SpotifyObject = Spotify(client_id, client_secret)
# TidalObject = Tidal()

# def convert_tidal_to_spotify(url):
#     track_info = TidalObject.get_track_info(url)
    
#     spotify_url = SpotifyObject.get_url(track_info)
#     return spotify_url

# def convert_spotify_to_tidal(url):
#     track_info = SpotifyObject.get_track_info(url)

#     tidal_info = TidalObject.get_url(track_info)
#     return tidal_info

# print('Tidal to Spotify:', convert_tidal_to_spotify('https://tidal.com/browse/track/1771732'))

# print('Spotify to Tidal:', convert_spotify_to_tidal('https://open.spotify.com/track/5zzWx7oJ9zBmv76uFaFeYR'))