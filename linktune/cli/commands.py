from linktune.api.convert import Convert
from linktune.api.search import Search

def convert(args):
    # get target service and song link from arguments
    service, link = args.target, args.link

    # call convert_link function from convert api
    converted_link = Convert().convert_link(link, service)
    if converted_link is None:
        print(f"Unable to find information for {link} on {service}")
    print(converted_link)

# def search(args):
#     artist, title, service = args.artist, args.title, args.service




# # class SearchCommand:
# #     @staticmethod
# #     def execute(args):
