import requests
import json

class Deezer:
    base_url = 'https://api.deezer.com/'

    def get_track_info(self, track_url):
        print('Searching for track...')
        track_id = self._get_track_id(track_url)

        query = f'{self.base_url}/track/{track_id}'
        response = requests.get(query)
        response.raise_for_status()

        data = response.json()

        title = data['title']
        artist = data['artist']['name']

        return {'artist': artist, 'title': title}


    # def get_url(self, info):

    def _get_track_id(self, track_url):
        _, _, track_id = track_url.rpartition('/')
        print(f'Track id is {track_id}')
        if not track_id:
            return "Could not locate track id"
        return track_id