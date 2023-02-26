from ytmusicapi import YTMusic
import re

# this can convert links to both YouTube Music and regular YouTube links
# as long as the id and externalID are the same...

class YouTube:
    def __init__(self):
        self.youtube = YTMusic()

    def get_track_info(self, track_url):
        print('Searching for track...')
        track_id = self._get_track_id(track_url)
        if not track_id:
            return 'Could not identify YouTube Music track ID from url.'

        track = self.youtube.get_song(track_id)
        # returns dictionary with song metadata
        artist = track['videoDetails']['author']
        title = track['videoDetails']['title']

        # TODO: implement integration with regular YouTube
        # external_video_id = track['microformat']

        return {'artist': artist, 'title': title}

# https://music.youtube.com/watch?v=tqxRidAWER8
    
    def _get_track_id(self, track_url):
        track_id = None
        track_id = re.search(r"v=([\w-]+)", track_url)
        track_id = track_id.group(1)

        return track_id
    
    def get_url(self, info):
        title = info['title']
        if isinstance(info['artist'], list):
            artist = info['artist'][0]
        else:
            artist = info['artist']

        # store top result of search
        res = self.youtube.search(f"{artist} {title}", filter = 'songs')[0]
        track_id = res['videoId']
        title = res['title']
        # TODO: edit artist to actually find all artist names in the array but this works for now
        artist = res['artists'][0]['name']

        return(f"info: {title} by {artist}: url: https://music.youtube.com/watch?v={track_id}")

# testing using regular youtube links from unofficial accounts... actually does work but really wouldnt be that great for non-verified artists
# I could make it take the track title from youtube and use that as the search query for other services?
# id = 'xAok29V8Bf4'
# yt = YouTube()
# print(yt.get_track_info('https://music.youtube.com/watch?v=xAok29V8Bf4'))