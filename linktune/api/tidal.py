import re
import requests
from tidal_unofficial import TidalUnofficial
from linktune.utils.exceptions import *


class Tidal:
    service_name = 'Tidal'
    def __init__(self):
        self.tidal = TidalUnofficial({'user_agent': 'my_user_agent'})

    def get_track_info(self, track_url):
        try:
            track_id = self._get_track_id(track_url)
        except TrackIdNotFoundException as e:
            raise e
        
        try:
            track = self.tidal.get_track(track_id)
        except requests.Timeout as e:
            raise ServiceTimeoutError("API request timed out.") from e
        if not track:
            raise InvalidLinkException("Provided link was not valid. Error returned by service.")
            
        title = track['title']
        artist = track['artist']['name']
        album = track['album']['title']

        return {'artist': artist, 'title': title, 'album': album}

    def _get_track_id(self, track_url):
        track_id = None
        try:
            track_id = track_url.split('/')[-1]
        except:
            raise TrackIdNotFoundException
        return track_id

    def get_service_url(self, info):
        query_type = info['query_type']
        title = re.sub("\(.*?\)|\[.*?\]","",info['title']).rstrip()
        if isinstance(info['artist'], list):
            artist = info['artist'][0]
        else:
            artist = info['artist']
        query = f"{title}+{artist}"     

        try:
            results = self.tidal.search(query, search_type='tracks', limit=5)
        except requests.Timeout as e:
            raise ServiceTimeoutError("API request timed out.") from e
        if len(results['items']) < 1:
            raise NoResultsReturnedException(f"No results found for {title} by {artist}.")

        top_track = None
        track_artist = []

        # get_service_url should handle results differently depending on if its being called from a convert or search query.
        # convert queries should attempt to match album from source url, but if they fail it should still return a track match.
        # search queries where album is specified by the user should return track not found on {album} on {service} if album is not found.
        
        # check if album has been supplied either by the source service or the user
        if 'album' in info:
            album = info['album'].strip()
            for item in results['items']:
                if artist.lower() in item['artist']['name'].lower() and title.lower() in item['title'].lower() and album.lower() in item['album']['title'].lower():
                    top_track = item
                    break
            # check if top_track is empty after conclusion of the loop, then return according to query_type.
            if top_track is None:
                if query_type == 'search':
                    raise TrackNotFoundOnAlbumException(f"Could not find track on the album '{album}'. To search across all albums, omit the album argument.") 
                # if query_type != search, return the top track that matches artist and title.
                for item in results['items']:
                    if artist.lower() in item['artist']['name'].lower() and title.lower() in item['title'].lower():
                        top_track = item
                        break
                    raise TrackNotFoundException(f'Could not find {title} by {artist}.')
        else:
            for item in results['items']:
                if artist.lower() in item['artist']['name'].lower() and title.lower() in item['title'].lower():
                    top_track = item
                    break
            else:
                raise TrackNotFoundException(f'Could not find {title} by {artist}.')
            
        # we loop through artists to handle the case where there are multiple artists for one song
        for artist in top_track['artists']:
            track_artist.append(artist['name'])
        
        return {'service': 'Tidal', 'title': top_track['title'], 'artist': track_artist, 'url': top_track['url']}
