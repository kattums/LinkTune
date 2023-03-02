from linktune.api.tidal import Tidal
from linktune.api.spotify import Spotify
from linktune.api.deezer import Deezer
from linktune.api.applemusic import AppleMusic
from linktune.api.youtube import YouTube
from linktune.config.config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET

class Convert:
    def __init__(self):
        # Initialise a map of the service apis with any associated credentials
        self.service_map = {
            'spotify': (Spotify, SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET),
            'tidal': (Tidal,),
            'deezer': (Deezer,),
            'apple': (AppleMusic,),
            'youtube': (YouTube,),
        }

    def convert_link(self, link, target_service):
        source_service = None

        # find service name in services map. initialise service with args if necessary
        #  and get track info
        for service_name, service_tuple in self.service_map.items():
            if service_name in link:
                source_service = service_tuple[0](*service_tuple[1:])
                break
        if not source_service:
            return f"Could not identify service from provided link. Please make sure it is supported."
        if source_service:
            track_info = source_service.get_track_info(link)

        # convert to all other services by looping through all services that are not source
        # and adding to results array
        # i could do the below more succinctly w list comprehension... think about it later
        service_urls = []
        services_to_convert = self.service_map.keys() if target_service == 'all' else [target_service]
        for service_name in services_to_convert:
            if service_name in link:
                continue  # skip the source service
            target_class, *target_args = self.service_map.get(service_name, (None,))
            target_match = target_class(*target_args)
            if track_info:
                info = target_match.get_service_url(track_info)
                service_urls.append({info['service']: info['url']})
        if service_urls:
            return {'title': track_info['title'], 'artist': track_info.get('artist'), 'service_url': service_urls}
        
        return f"Could not convert link to {target_service}."
    
    # pretty_print takes a result from convert_link() and formats for display in the CLI
    def pretty_print(self, results):
        artist, title, service_urls = results['artist'], results['title'], results['service_url']
        
        
        pretty_results = f"{title} by {artist}\n"
        for service_url in service_urls:
            for service, url in service_url.items():
                pretty_results += f"{service}: {url}\n"
        return pretty_results.strip()

# TODO: unify the results we get from each music service
# TODO: implement services into a single super class
# TODO: change Convert() to not be a class anymore