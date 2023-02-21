import argparse

def create_parser():
    parser = argparse.ArgumentParser(description="LinkTune: Convert music links from one service to another and search for tracks across services.")
    subparsers = parser.add_subparsers(help='Commands', dest='command')

    # Convert command
    convert_parser = subparsers.add_parser('convert', help='Convert a music link to that of another music service.')
    convert_parser.add_argument('link', help='The link to be converted.')
    convert_parser.add_argument('target', help='The target music service to convert to.')

    # TODO: implement search command after implementing search in the API
    # search_parser = subparsers.add_parser('search', help='Search for a track by artist and title on a music service.')
    # search_parser.add_argument('--artist', '-a', help='Artist name')
    # search_parser.add_argument('--title', '-t', help='Track title')
    # search_parser.add_argument('--service', '-s', choices=['spotify', 'tidal', 'all'], default='all', help='The music service to search.')

    return parser