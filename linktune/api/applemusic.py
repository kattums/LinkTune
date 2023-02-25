import requests

class AppleMusic:

    itunes_base = 'https://itunes.apple.com/'

    def get_track_info(self, track_url):
        track_id = self._get_track_id(track_url)

        query = f'{self.itunes_base}lookup?id={track_id}'

        res = requests.get(query)
        res.raise_for_status()

        # get results dict from the json response
        data = res.json()['results'][0]

        title = data['trackName']
        artist = data['artistName']
        return {'artist': artist, 'title': title}

    def _get_track_id(self, track_url):
        track_id = track_url.split('?i=')[1]
        if not track_id:
            return "Could not locate track id"
        return track_id
    
    def get_url(self, info):
        title = info['title']
        if isinstance(info['artist'], list):
            artist = info['artist'][0]
        else:
            artist = info['artist']

        query = f'{self.itunes_base}search?term={artist}+{title}'

        res = requests.get(query)
        res.raise_for_status()

        # get json response of matching tracks
        data = res.json()['results'][0]

        link, artist, title = data['trackViewUrl'], data['artistName'], data['trackName']

        return f'{title} ' 'by ' f'{artist}'': ' f'{link}'