import re
import requests
from ytmusicapi import YTMusic
from linktune.utils.exceptions import *

class YouTube:
    """Class to represent YouTube Music API service.
    
    Attributes:
        service_name (str):
            name of the service.

    Methods:
        get_track_info(track_url):
            Returns info of provided YouTube Music track (artist, title, album).
        _get_track_id(track_url):
            Helper function for get_track_url. Returns track ID from track URL.
        get_service_url(info):
            Returns YouTube Music URL when provided with artist and track information to query.
    """
    service_name = 'YouTube Music'
    def __init__(self):
        self.youtube = YTMusic()

    def get_track_info(self, track_url):
        """Retrieves track information from a given YouTube Music URL.

        Args:
            track_url (str): YouTube Music url provided by the user. 
            example: "https://music.youtube.com/watch?v=SYto6vfUwXo"

        Raises:
            TrackIdNotFound: propagated from _get_track_id track ID cannot be identified.
            ServiceTimeoutError: Raised when API response times out.
            InvalidLinkException: Raised when user provides an invalid URL that contains 'youtube'

        Returns:
            dict: track info object containing artist, track title, 
            and album information obtained from YouTube Music API.
        """
        try:
            track_id = self._get_track_id(track_url)
        except TrackIdNotFoundException as e:
            raise e
        
        try:
            track = self.youtube.search(track_id, filter='songs')[0]
        except requests.Timeout:
            raise ServiceTimeoutError("API request timed out.")
        except IndexError:
            raise InvalidLinkException('Could not identify track from provided link.')

        artist = [artist['name'] for artist in track['artists']]
        title, album = track['title'], track['album']['name']
        return {'artist': artist, 'title': title, 'album': album}

    def _get_track_id(self, track_url):
        """Identifies track ID from a provided YouTube Music URL.

        Args:
            track_url (str): YouTube Music url provided by the user. 
            example: "https://music.youtube.com/watch?v=SYto6vfUwXo" where "SYto6vfUwXo" is track ID.

        Raises:
            TrackIdNotFoundException: raised when track ID cannot be identified from provided URL.

        Returns:
            str: track ID, e.g. "SYto6vfUwXo".
        """
        track_id = None
        try:
            track_id = re.search(r"v=([\w-]+)", track_url)
            track_id = track_id.group(1)
        except track_id is None:
            raise TrackIdNotFoundException('Could not identify track ID from provided link.')
        return track_id

    def get_service_url(self, info):
        """Queries the YouTube Music API with provided track info in order to obtain the track
        URL on the YouTube Music service.

        Args:
            info (dict): contains the following keys:
                artist: artist name
                title: track title
                album: album title [OPTIONAL KEY]
                query_type: type of calling function - opts 'convert' or 'search'.

        Raises:
            ServiceTimeoutError: when API response times out.
            TrackNotFoundOnAlbumException: track cannot be located on specified album 
            with query_type == 'search'.
            TrackNotFoundException: when the track cannot be found on the service.

        Returns:
            dict: returns a dictionary result containing service name, artist name, track title, 
            and the URL for the track.
        """
        query_type = info['query_type']
        title = re.sub("\(.*?\)|\[.*?\]","",info['title']).rstrip()
        if isinstance(info['artist'], list):
            artist = info['artist'][0]
        else:
            artist = info['artist']

        query = f"{artist} {title}"
        if 'album' in info:
            album = info['album']
            query += f" {album}"

        try:
            top_tracks = self.youtube.search(f"{artist} {title}", filter = 'songs', limit = 5)
        except requests.Timeout:
            raise ServiceTimeoutError("API request timed out.")

        top_track = None

        if 'album' in info:
            for track in top_tracks:
                if artist.lower() in track['artists'][0]['name'].lower() and title.lower() in track['title'].lower() and album.lower() in track['album']['name'].lower():
                    top_track = track
                    break
            # check if top_track is empty after conclusion of the loop, then return according to query_type.
            if top_track is None:
                if query_type == 'search':
                    raise TrackNotFoundOnAlbumException(f"Could not find track on the album '{album}'. To search across all albums, omit the album argument.") 
                for track in top_tracks:
                    if artist.lower() in track['artists'][0]['name'].lower() and title.lower() in track['title'].lower():
                        top_track = track
                        break
                    raise TrackNotFoundException(f'Could not find {title} by {artist}.')       
        else:
            for track in top_tracks:
                if artist.lower() in track['artists'][0]['name'].lower() and title.lower() in track['title'].lower():
                    top_track = track
                    break
            else:
                raise TrackNotFoundException(f'Could not find {title} by {artist}.')

        track_id, track_title, track_artist = top_track['videoId'], top_track['title'], [artist['name'] for artist in top_track['artists']]

        return {'service': 'YouTube Music', 'title': track_title, 'artist': track_artist, 'url': f"https://music.youtube.com/watch?v={track_id}"}