from linktune.api.convert import Convert
from linktune.api.search import search_track, pretty_print
from linktune.utils.exceptions import *

def convert(args):
    # get target service and song link from arguments
    service, link = args.target.lower(), args.link
    converted_result = {}
    
    # call convert_link function from convert api
    try:
        converted_result = Convert().convert_link(link, service)
        print(Convert().pretty_print(converted_result))
    except ServiceNotFoundException as e:
        print(e)
        
    if converted_result is None: # this needs some refactoring
        print(f"Unable to find information for {link} on {service}")
        
    return

def search(args):
    artist, title = args.artist.lower(), args.title.lower()
    service = args.service.lower() if args.service else None
    album = args.album.lower() if args.album else None
    print(pretty_print(search_track(artist, title, service, album)))
    return