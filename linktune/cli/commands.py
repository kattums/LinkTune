# import sys
# from linktune.cli.arguments import create_parser
# from linktune.api import Convert
# # from linktune.cli.arguments import convert_arguments, search_arguments

# # ConvertCommand ; SearchCommand ; 

# class ConvertCommand:
#     @staticmethod
#     def execute(args):
#         service = args.service
#         url = args.url

#         converted_url = Convert.convert_link(url, service)
#         if converted_url is None:
#             print(f"Unable to find information for {url} on {service}")
#         print(converted_url)

# # class SearchCommand:
# #     @staticmethod
# #     def execute(args):
