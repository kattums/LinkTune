from linktune.api.convert import Convert
from linktune.api.search import search_track, pretty_print
from linktune.utils.exceptions import *

def convert(args):
    print('Searching for track...')
    # get target service and song link from arguments
    service, link = args.target.lower(), args.link
    converted_result = {}
    
    # call convert_link function from convert api
    try:
        converted_result = Convert().convert_link(link, service)
        print(Convert().pretty_print(converted_result))
    except (ServiceNotFoundException, InvalidLinkException, TrackIdNotFoundException) as e:
        print(str(e))
        
    if converted_result is None: 
        raise ConvertLinkException('An unknown error occurred during conversion.')


def search(args):
    artist, title = args.artist.lower(), args.title.lower()
    service = args.service.lower() if args.service else None
    album = args.album.lower() if args.album else None
    result = {}
    
    try:
        result = search_track(artist, title, service, album)
        print(pretty_print(result))
    except (ServiceTimeoutError, NoResultsReturnedException, TrackNotFoundException, TrackNotFoundOnAlbumException) as e:
        print(str(e))
        
    if result is None:
        raise SearchException('An unknown error occurred during search.')