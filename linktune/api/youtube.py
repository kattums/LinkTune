from ytmusicapi import YTMusic
import re

# this can convert links to both YouTube Music and regular YouTube links
# as long as the id and externalID are the same...

class YouTube:
    service_name = 'YouTube Music'
    def __init__(self):
        self.youtube = YTMusic()

    def get_track_info(self, track_url):
        print('Searching for track...')
        track_id = self._get_track_id(track_url)
        if not track_id:
            return 'Could not identify YouTube Music track ID from url.' # this error doesnt work need to fix

        track = self.youtube.search(track_id)[0]
        # returns dictionary with song metadata
        artist = [artist['name'] for artist in track['artists']]
        title = track['title']
        album = track['album']['name']

        # TODO: implement integration with regular YouTube
        # external_video_id = track['microformat']

        return {'artist': artist, 'title': title, 'album': album}

# https://music.youtube.com/watch?v=tqxRidAWER8
    
    def _get_track_id(self, track_url):
        track_id = None
        track_id = re.search(r"v=([\w-]+)", track_url)
        track_id = track_id.group(1)

        return track_id
    
    def get_service_url(self, info):
        title = info['title']
        if isinstance(info['artist'], list):
            artist = info['artist'][0]
        else:
            artist = info['artist']

        query = f"{artist} {title}"
        if 'album' in info:
            query += f" {info['album']}"
        # store top result of search
        top_track = self.youtube.search(f"{artist} {title}", filter = 'songs')[0]
        track_id = top_track['videoId']
        track_title = top_track['title']
        track_artist = []
        for artist in top_track['artists']:
            track_artist.append(artist['name'])

        return {'service': 'YouTube Music', 'title': track_title, 'artist': track_artist, 'url': f"https://music.youtube.com/watch?v={track_id}"}
# testing using regular youtube links from unofficial accounts... actually does work but really wouldnt be that great for non-verified artists
# I could make it take the track title from youtube and use that as the search query for other services?
# id = 'xAok29V8Bf4'
# yt = YouTube()
# print(yt.get_track_info('https://music.youtube.com/watch?v=xAok29V8Bf4'))