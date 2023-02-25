import requests

class AppleMusic:
    base_url = 'https://music.apple.com/gb/album/'

# example applemusic: https://music.apple.com/gb/album/mockingbird/1452852431?i=1452852850
# needs TWO ids. string after album is song name.

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