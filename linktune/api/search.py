from linktune.api.tidal import Tidal
from linktune.api.spotify import Spotify
from linktune.api.deezer import Deezer
from linktune.api.applemusic import AppleMusic
from linktune.api.youtube import YouTube
from linktune.config.config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET

def search_track(artist, title, service='all'):
    info = {'title': title, 'artist': artist}

    service_map = {
        'spotify': (Spotify, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET),
        'tidal': (Tidal,),
        'deezer': (Deezer,),
        'apple': (AppleMusic,),
        'youtube': (YouTube,),
    }

    if service == 'all':
        results = []
        for service in service_map:
            service_class, *service_args = service_map.get(service, (None,))
            api = service_class(*service_args)
            results.append(f"{service}: {api.get_url(info)}")
        return results

    if service in service_map:
        service_class, *service_args = service_map.get(service, (None,))
        api = service_class(*service_args)
        return api.get_url(info)
    else:
        return "Service not supported"

