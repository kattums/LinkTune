import requests

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

    def _get_track_id(self, track_url):
        _, _, track_id = track_url.rpartition('/')
        print(f'Track id is {track_id}')
        if not track_id:
            return "Could not locate track id"
        return track_id
    
    def get_service_url(self, info):
        title = info['title']
        artist = info['artist']

        query = f'{self.base_url}/search?q=artist:"{artist}" track:"{title}"'
        response = requests.get(query)
        response.raise_for_status()

        top_track = response.json()['data'][0]
        track_title = top_track['title']
        track_link = top_track['link']
        track_artists = [top_track['artist']]
        track_artist = [artist['name'] for artist in track_artists]
        
        return {'service': 'Deezer', 'title': track_title, 'artist': track_artist, 'url': track_link}
