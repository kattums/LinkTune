import argparse
from linktune.api.convert import Convert

# create command-line argument parser
parser = argparse.ArgumentParser(description='Convert URLs from one music service to another')

#  add arguments for the URL to convert and target music service to convert to
parser.add_argument('url', help='the URL to convert')
parser.add_argument('target', help='the target music service to convert to.')

# parse the command-line arguments
args = parser.parse_args()

converter = Convert()
url = converter.convert_link(args.url, args.target)