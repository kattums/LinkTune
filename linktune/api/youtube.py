from ytmusicapi import YTMusic
import re
import requests
from linktune.utils.exceptions import *

# this can convert links to both YouTube Music and regular YouTube links
# as long as the id and externalID are the same...

class YouTube:
    service_name = 'YouTube Music'
    def __init__(self):
        self.youtube = YTMusic()

    def get_track_info(self, track_url):
        try:
            track_id = self._get_track_id(track_url)
        except TrackIdNotFoundException as e:
            raise e
        
        try:
            track = self.youtube.search(track_id, filter='songs')[0]
        except requests.Timeout:
            raise ServiceTimeoutError(f"API request timed out.")
        except IndexError:
            raise InvalidLinkException('Could not identify track from provided link.')

        artist = [artist['name'] for artist in track['artists']]
        title, album = track['title'], track['album']['name']
        return {'artist': artist, 'title': title, 'album': album}

    def _get_track_id(self, track_url):
        track_id = None
        try:
            track_id = re.search(r"v=([\w-]+)", track_url)
            track_id = track_id.group(1)
        except track_id is None:
            raise TrackIdNotFoundException('Could not identify track ID from provided link.')
        return track_id
    
    def get_service_url(self, info):
        title = re.sub("\(.*?\)|\[.*?\]","",info['title']).rstrip()
        if isinstance(info['artist'], list):
            artist = info['artist'][0]
        else:
            artist = info['artist']

        query = f"{artist} {title}"
        if 'album' in info:
            query += f" {info['album']}"
            
        try:
            top_track = self.youtube.search(f"{artist} {title}", filter = 'songs')[0]
        except IndexError:
            raise TrackNotFoundException(f'No results found for {title} by {artist}.')
        except requests.Timeout:
            raise ServiceTimeoutError(f"API request timed out.")
        
        track_id, track_title, track_artist = top_track['videoId'], top_track['title'], [artist['name'] for artist in top_track['artists']]

        return {'service': 'YouTube Music', 'title': track_title, 'artist': track_artist, 'url': f"https://music.youtube.com/watch?v={track_id}"}

