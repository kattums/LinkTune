from arguments import create_parser
from linktune.api.convert import Convert

# create command-line argument parser
parser = create_parser()
args = parser.parse_args()

converter = Convert()
track = converter.convert_link(args.link, args.target)
print(track['info'], track['url'])