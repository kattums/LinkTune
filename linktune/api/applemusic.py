import requests

class AppleMusic:

    itunes_base = 'https://itunes.apple.com/'
    service_name = 'Apple Music'

    def get_track_info(self, track_url):
        track_id = self._get_track_id(track_url)

        query = f'{self.itunes_base}lookup?id={track_id}'

        res = requests.get(query, timeout=2)
        res.raise_for_status()

        # get results dict from the json response
        data = res.json()['results'][0]

        title = data['trackName']
        artist = data['artistName']
        album = data['collectionName']
        return {'artist': artist, 'title': title, 'album': album}

    def _get_track_id(self, track_url):
        track_id = track_url.split('?i=')[1]
        if not track_id:
            return "Could not locate track id"
        return track_id
    
    def get_service_url(self, info):
        title = info['title']
        
        if isinstance(info['artist'], list):
            artist = info['artist'][0]
        else:
            artist = info['artist']

        query = f"{self.itunes_base}search?term={artist}+{title}"

        if 'album' in info:
            query += f"+{info['album']}"

        res = requests.get(query, timeout=2)
        res.raise_for_status()

        data = res.json()
        # get json response of matching tracks
        if data['results']: 
            top_track = data['results'][0]

            link, artist, title = top_track['trackViewUrl'], [top_track['artistName']], top_track['trackName']

            return {'service': 'Apple Music', 'title': title, 'artist': artist, 'url': link}
        return None