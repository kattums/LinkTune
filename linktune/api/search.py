from linktune.api.tidal import Tidal
from linktune.api.spotify import Spotify
from linktune.api.deezer import Deezer
from linktune.api.applemusic import AppleMusic
from linktune.config.config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET

# TODO: implement map of services for quicker look up; add "all" option which is the default
def search_track(artist, title, service='all'):
    info = {'title': title, 'artist': artist}

    api_map = {
        'spotify': (Spotify, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET),
        'tidal': (Tidal,),
        'deezer': (Deezer,),
        'apple': (AppleMusic,),
    }

    if service == 'all':
        results = []
        for service in api_map:
            api_args = api_map[service]
            api_class = api_args[0]
            api = api_class(*api_args[1:])
            results.append(f"{service}: {api.get_url(info)}")
        return results

    if service in api_map:
        api_args = api_map[service]
        api_class = api_args[0]
        api = api_class(*api_args[1:])
        return api.get_url(info)
    else:
        return "Service not supported"

