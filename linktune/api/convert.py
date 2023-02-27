from linktune.api.tidal import Tidal
from linktune.api.spotify import Spotify
from linktune.api.deezer import Deezer
from linktune.api.applemusic import AppleMusic
from linktune.api.youtube import YouTube
from linktune.config.config import SPOTIPY_CLIENT_ID, SPOTIPY_CLIENT_SECRET

class Convert:
    def __init__(self):
        # Initialise a map of the service apis
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
        if target_service == 'all':
            results = []
            for service_name in self.service_map.keys():
                if service_name in link:
                    continue  # skip the source service
                target_class, *target_args = self.service_map.get(service_name, (None,))
                target_match = target_class(*target_args)
                if track_info:
                    info = target_match.get_url(track_info)
                    results.append(f"{service_name}: {info['title']} by {info['artist']}: {info['url']}")
            return results
        else:
            if track_info:
                target_class, *target_args = self.service_map.get(target_service, (None,))
                target_match = target_class(*target_args)
                info = target_match.get_url(track_info)
                return f"{info['title']} by {info['artist']}: {info['url']}"

        return f"Something went wrong during conversion."
    

