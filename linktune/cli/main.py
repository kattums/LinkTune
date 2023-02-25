from linktune.cli.arguments import create_parser

def main():
    parser = create_parser()

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    args.func(args)

if __name__ == '__main__':
    main()