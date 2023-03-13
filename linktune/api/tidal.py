from tidal_unofficial import TidalUnofficial
import re
import sys

class Tidal:
    service_name = 'Tidal'
    def __init__(self):
        self.tidal = TidalUnofficial({'user_agent': 'my_user_agent'})

    def get_track_info(self, track_url):
        track_id = self._get_track_id(track_url)
        if not track_id:
            return None
        track = self.tidal.get_track(track_id)
        title = track['title']
        artist = track['artist']['name']
        album = track['album']['title']

        return {'artist': artist, 'title': title, 'album': album}

    def _get_track_id(self, track_url):
        track_id = None
        if 'tidal' in track_url:
            track_id = track_url.split('/')[-1]
        return track_id

    def get_service_url(self, info):
        query_type = info['query_type']
        
        title = re.sub("\(.*?\)|\[.*?\]","",info['title']).rstrip()
        if isinstance(info['artist'], list):
            artist = info['artist'][0]
        else:
            artist = info['artist']
        query = f"{title}+{artist}"        

        results = None
        results = self.tidal.search(query, search_type='tracks', limit=5)

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
            if top_track == None:
                if query_type == 'search':
                    print('could not find track on album') # TODO: handle this properly
                else: # if query_type != search, return the top track that matches artist and title.
                    for item in results['items']:
                        if artist.lower() in item['artist']['name'].lower() and title.lower() in item['title'].lower():
                            top_track = item
                            break
                    
        else:
            for item in results['items']:
                if artist.lower() in item['artist']['name'].lower() and title.lower() in item['title'].lower():
                    top_track = item
                    break
            
        # we loop through artists to handle the case where there are multiple artists for one song
        for artist in top_track['artists']:
            track_artist.append(artist['name'])
            return {'service': 'Tidal', 'title': top_track['title'], 'artist': track_artist, 'url': top_track['url']}
        return f"Could not find track {title} by {artist} on Tidal."