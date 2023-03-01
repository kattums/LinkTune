from linktune.api.convert import Convert
from linktune.api.search import search_track

def convert(args):
    # get target service and song link from arguments
    service, link = args.target, args.link

    # call convert_link function from convert api
    converted_result = Convert().convert_link(link, service)
    if converted_result is None:
        print(f"Unable to find information for {link} on {service}")
    print(Convert().pretty_print(converted_result))

def search(args):
    artist, title, service = args.artist, args.title, args.service

    print(search_track(artist, title, service))