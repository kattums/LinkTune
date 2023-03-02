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

    def get_service_url(self, info):
        title = info['title']
        if isinstance(info['artist'], list):
            artist = info['artist'][0]
        else:
            artist = info['artist']
        query = f"{title}"

        result = None
        result = self.tidal.search(query, search_type='tracks', limit=1)
        # BUG need to check top track better, getting wrong result for Everybody's Gotta Live. temp fix just search track

        # check if we have any results, and if so take the top result returned by the API
        if len(result['items']) > 0:
            top_track = result['items'][0]
            track_artist = []
            # we loop through artists to handle the case where there are multiple artists for one song
            for artist in top_track['artists']:
                track_artist.append(artist['name'])
            return {'service': 'Tidal', 'title': top_track['title'], 'artist': track_artist, 'url': top_track['url']}
        return f"Could not find track {title} by {artist} on Tidal."