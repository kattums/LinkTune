import requests
import re
import json
from bs4 import BeautifulSoup
from linktune.utils.exceptions import *

class Deezer:
    service_name = 'Deezer'
    base_url = 'https://api.deezer.com/'

    def get_track_info(self, track_url):
        if 'page' in track_url:
            return self._parse_sharelink(track_url)

        try:
            track_id = self._get_track_id(track_url)
        except TrackIdNotFoundException as e:
            raise e

        query = f'{self.base_url}/track/{track_id}'

        try:
            response = requests.get(query)
            response.raise_for_status()
        except requests.Timeout as e:
            raise ServiceTimeoutError("API request timed out.") from e
        if response.status_code != 200:
            raise ServiceResponseError("The service response produced an error.")

        data = response.json()

        if 'error' in data:
            raise InvalidLinkException("Provided link was not valid. Error returned by service.")

        title, artist, album = data['title'], data['artist']['name'], data['album']['title']

        return {'artist': artist, 'title': title, 'album': album}

    def _get_track_id(self, track_url):
        try:
            _, _, track_id = track_url.rpartition('/')
        except:
            raise TrackIdNotFoundException('Could not identify track ID from provided link.')
        return track_id

    def _parse_sharelink(self, track_url):
        response = requests.get(track_url, timeout=2)
        if response.status_code != 200:
            return None

        soup = BeautifulSoup(response.text, 'html.parser')

        script_data = soup.find_all('script', string=lambda t: t and 
                                    'window.__DZR_APP_STATE__' in t)[0].text.replace(
                                    'window.__DZR_APP_STATE__ =', '').strip()

        if not script_data or len(script_data) == 0 or script_data == "":
            return None

        try:
            normalized_data = json.loads(script_data)['DATA']
            if not normalized_data:
                return None

            title, artist, album = (normalized_data['SNG_TITLE'],
                                    normalized_data['ART_NAME'], normalized_data['ALB_TITLE'])
            return {'artist': artist, 'title': title, 'album': album}

        except json.JSONDecodeError:
            return None

    def get_service_url(self, info):
        title = re.sub("\(.*?\)|\[.*?\]","",info['title']).rstrip()
        artist = info['artist']

        query = f'{self.base_url}/search?q=artist:"{artist}"track:"{title}"'
        if 'album' in info:
            album = info['album']
            query += f'album:"{album}"'

        try:
            response = requests.get(query, timeout=2)
            response.raise_for_status()
        except requests.Timeout as e:
            raise ServiceTimeoutError("API request timed out.") from e
        if response.status_code != 200:
            raise ServiceResponseError("The service response produced an error.")

        if response.json()['total'] < 1:
            raise TrackNotFoundException(f'No results found for {title} by {artist}.')
        print(response.json())
        data = response.json()['data']
        top_track = data[0]

        track_title, track_link = top_track['title'], top_track['link']
        track_artists = [top_track['artist']]
        track_artist = [artist['name'] for artist in track_artists]

        return {'service': 'Deezer', 'title': track_title,
                'artist': track_artist, 'url': track_link}
