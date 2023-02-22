from linktune.api.convert import Convert
from linktune.api.search import search_track

def convert(args):
    # get target service and song link from arguments
    service, link = args.target, args.link

    # call convert_link function from convert api
    converted_link = Convert().convert_link(link, service)
    if converted_link is None:
        print(f"Unable to find information for {link} on {service}")
    print(converted_link)

def search(args):
    artist, title, service = args.artist, args.title, args.service

    print(search_track(artist, title, service))