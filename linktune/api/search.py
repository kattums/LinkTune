from linktune.api.tidal import Tidal
from linktune.api.spotify import Spotify
from linktune.config.config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET

# TODO: implement map of services for quicker look up; add "all" option which is the default
def search_track(artist, title, service='all'):
    info = {'title': title, 'artist': artist}
    if service == 'spotify':
        spotify = Spotify(SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET)
        return spotify.get_url(info)
    elif service == 'tidal':
        tidal = Tidal()
        return tidal.get_track_url(info)
    else:
        return "Something broke"