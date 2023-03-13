from linktune.api.tidal import Tidal
from linktune.api.spotify import Spotify
from linktune.api.deezer import Deezer
from linktune.api.applemusic import AppleMusic
from linktune.api.youtube import YouTube
from linktune.config.config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET
from linktune.utils.exceptions import *

def search_track(artist, title, service='all', album=None):
    service_map = {
    'spotify': (Spotify, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET),
    'tidal': (Tidal,),
    'deezer': (Deezer,),
    'apple': (AppleMusic,),
    'youtube': (YouTube,),
}

    info = {'title': title, 'artist': artist}
    if album is not None:
        info['album'] = album
    info['query_type'] = 'search'
    
    results = {}
    service_urls = []
    found_artist = found_title = False

    search_service = [s for s in service_map.keys() if service == 'all' or s == service]
    if service != 'all' and service not in service_map:
        raise ServiceNotFoundException(f"{service} is not a supported service.")
    
    for service_name in search_service:
        service_class, *service_args = service_map.get(service_name, (None,))
        api = service_class(*service_args)
        
        details = {}
        try: 
            details = api.get_service_url(info)
        except TrackNotFoundOnAlbumException as e:
            if service != 'all':
                raise e
            continue # TODO: fix this behaviour for when its only not found on ONE
            
        if not found_artist:
            track_artist = details.get('artist')
            found_artist = True
        if not found_title:
            track_title = details.get('title')
            found_title = True
        service_urls.append({details['service']: details['url']})
    results.update({'service_url': service_urls})
    if results:
        if track_artist:
            results['artist'] = track_artist
        if track_title:
            results['title'] = track_title
    return results


def pretty_print(results):
    artists, title, service_urls = results['artist'], results['title'], results['service_url']
    # List comprehension to correctly format for multiple artists, else get the single artist element in the list
    artist = f"{', '.join(artists)}" if len(artists) > 1 else artists[0]

    pretty_results = f"{title} by {artist}\n"
    for service_url in service_urls:
        for service, url in service_url.items():
            pretty_results += f"{service}: {url}\n"
    return pretty_results.strip()