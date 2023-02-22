from linktune.api.tidal import Tidal
from linktune.api.spotify import Spotify
import os

client_id = os.environ.get('SPOTIPY_CLIENT_ID')
client_secret = os.environ.get('SPOTIPY_CLIENT_SECRET')

# given an artist name, track title, and target service, search should locate track and return links. default value for target is all.
# if 'all', then return links for all services

# TODO: implement map of services for quicker look up; add "all" option which is the default; remove api keys from code
def search_track(artist, title, service='all'):
    info = {'title': title, 'artist': artist}
    if service == 'spotify':
        spotify = Spotify(client_id, client_secret)
        return spotify.get_url(info)
    elif service == 'tidal':
        tidal = Tidal()
        return tidal.get_track_url(info)
    else:
        return "Something broke"