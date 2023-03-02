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

    results = []

    if service == 'all':
        for service in service_map:
            service_class, *service_args = service_map.get(service, (None,))
            api = service_class(*service_args)
            results.append(f"{service}: {api.get_url(info)}")
        return results

    elif service in service_map:
        service_class, *service_args = service_map.get(service, (None,))
        api = service_class(*service_args)
        results.append(f"'service': {service}, {api.get_url(info)}")
        return results
    else:
        return "Service not supported"

# TODO: implement pretty_print for search
# TODO: I think I should make it so each service returns its own service name with its results...
# def pretty_print(results):
#     artist, title, urls = results['artist'], results['title'], results['url']
#     pretty_results = f"{artist} - {title}\n"
#     for url in urls:
#         pretty_results += f"{url}\n"
#     return pretty_results.strip()