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
        # check if target_service provided. use tuple unpacking to
        # initialise class from the service map and unpack its args.
        if target_service:
            target_class, *target_args = self.service_map.get(target_service, (None,))
            target_match = target_class(*target_args)
            for service_name, service_tuple in self.service_map.items():
                if service_name in link:
                    source_service = service_tuple[0](*service_tuple[1:])
                    break

            if source_service:
                track_info = source_service.get_track_info(link)
                if track_info:
                    info = target_match.get_url(track_info)
                    return f"{info['title']} by {info['artist']}: {info['url']}"

        return "Something went wrong during conversion."