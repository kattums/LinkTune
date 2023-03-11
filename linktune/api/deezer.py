import requests
import re

class Deezer:
    service_name = 'Deezer'
    base_url = 'https://api.deezer.com/'

    def get_track_info(self, track_url):
        print('Searching for track...')
        track_id = self._get_track_id(track_url)

        query = f'{self.base_url}/track/{track_id}'

        try:
            response = requests.get(query)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return f"Could not retrieve track information from Deezer: {str(e)}"

        data = response.json()
        # print(data)
        # if 'error' in data:
        #     raise SystemExit(f"No results returned for the Deezer url: {track_url}. Please ensure the link is valid.")
        title = data['title']
        artist = data['artist']['name']
        album = data['album']['title']

        return {'artist': artist, 'title': title, 'album': album}

    def _get_track_id(self, track_url):
        _, _, track_id = track_url.rpartition('/')
        if not track_id:
            return "Could not locate track id"
        return track_id
    
    def get_service_url(self, info):
        title = re.sub("\(.*?\)|\[.*?\]","",info['title']).rstrip()
        artist = info['artist']

        query = f'{self.base_url}/search?q=artist:"{artist}"track:"{title}"'
        if 'album' in info:
            album = info['album']
            query += f'album:"{album}"'
            
        response = requests.get(query)
        response.raise_for_status()

        # I think perhaps the better way to handle this is to still return the object but instead of
        # "url: url" I can put "url: could not find track" into the dict.
        data = response.json()['data']
        if not data:
            return None

        top_track = data[0]
        track_title = top_track['title']
        track_link = top_track['link']
        track_artists = [top_track['artist']]
        track_artist = [artist['name'] for artist in track_artists]
        
        return {'service': 'Deezer', 'title': track_title, 'artist': track_artist, 'url': track_link}
