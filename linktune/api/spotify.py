import spotipy
import re
import requests
from spotipy.oauth2 import SpotifyClientCredentials
from spotipy.cache_handler import MemoryCacheHandler
from linktune.utils.exceptions import *


class Spotify:
    service_name = 'Spotify'
    def __init__(self, client_id, client_secret):
        self.sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret, cache_handler=MemoryCacheHandler()))

    def get_track_info(self, track_url):
        try:
            track_id = self._get_track_id(track_url)
        except TrackIdNotFoundException as e:
            raise e

        try:
            track = self.sp.track(track_id)
        except requests.Timeout:
            raise ServiceTimeoutError("API request timed out.")
        if not track: # reconsider this implementation... its not strictly true.
            raise InvalidLinkException("Provided link was not valid. Error returned by service.")
        
        artists = [artist['name'] for artist in track['artists']]
        title = track['name']
        album = track['album']['name']

        return {'artist': artists[0], 'title': title, 'album': album}

    def _get_track_id(self, track_url):
        track_id = None
        try:
            # check if Spotify internal id is appended to the link and remove if so
            if '?si=' in track_url:
                track_url = track_url.split('?si=')[0]
            if 'open.spotify.com/track/' in track_url:
                _, _, track_id = track_url.rpartition('/')
            elif 'spotify:track:' in track_url:
                _, _, track_id = track_url.rpartition(':')
        except:
            raise TrackIdNotFoundException("Could not identify track ID from provided link.")
        return track_id

    def get_service_url(self, info):
        # remove extra and paranthesied characters present in track title
        title = re.sub("\(.*?\)|\[.*?\]","",info['title']).rstrip()

        if isinstance(info['artist'], list):
            artist = info['artist'][0]
        else:
            artist = info['artist']
        
        query_type = info['query_type']

        query = f"track:{info['title']} artist:{artist}"
                
        if 'album' in info:
            album = info['album']
            query += f" album:{info['album']}"

        try:
            results = self.sp.search(query, limit=10, type='track')
        except requests.Timeout:
            raise ServiceTimeoutError("API request timed out.")
        if len(results['tracks']['items']) < 1:
            raise NoResultsReturnedException(f"No results found for {title} by {artist}.")
        
        # print(results['tracks']['items'])
        
        top_track = None
        
        if 'album' in info:
            for item in results['tracks']['items']:
                if artist.lower() in item['artists'][0]['name'].lower() and title.lower() in item['name'].lower() and album.lower() in item['album']['name'].lower():
                    top_track = item
                    break
                if top_track is None:
                    if query_type == 'search':
                        raise TrackNotFoundOnAlbumException(f"Could not find track on the album '{album}'. To search across albums, omit the album argument.")
                    else:
                        for item in results['items']:
                            print(item)
                            if artist.lower() in item['artists'][0]['name'].lower() and title.lower() in item['name'].lower():
                                top_track = item
                                break
        else:
            for item in results['tracks']['items']:
                if artist.lower() in item['artists'][0]['name'].lower() and title.lower() in item['name'].lower():
                    top_track = item
                    break
            else:
                raise TrackNotFoundException(f"Could not find {title} by {artist}.")

        track_artist, track_title, track_url = [artist['name'] for artist in top_track['artists']], top_track['name'], top_track['external_urls']['spotify']
        return {'service': 'Spotify', 'title': track_title, 'artist': track_artist, 'url': track_url}

