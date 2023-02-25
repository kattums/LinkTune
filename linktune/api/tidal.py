from tidal_unofficial import TidalUnofficial


class Tidal:
    def __init__(self):
        self.tidal = TidalUnofficial({'user_agent': 'my_user_agent'})

    def get_track_info(self, track_url):
        track_id = self._get_track_id(track_url)
        if not track_id:
            return None
        track = self.tidal.get_track(track_id)
        title = track['title']
        artist = track['artist']['name']

        return {'artist': artist, 'title': title}

    def _get_track_id(self, track_url):
        track_id = None
        track_id = track_url.split('/')[-1]
        return track_id

    def get_url(self, info):
        title = info['title']
        if isinstance(info['artist'], list):
            artist = info['artist'][0]
        else:
            artist = info['artist']
        query = f"{title} {artist}"

        result = self.tidal.search(query, search_type='tracks', limit=1)
        return f"info: {title} by {artist}, url: {result['items'][0]['url']}"