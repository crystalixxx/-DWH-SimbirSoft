from utils.database.core import DatabaseSender, create_all_tables

from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    parse_create = subparsers.add_parser('create_tables')

    parser_task = subparsers.add_parser('add_new_url')
    parser_task.add_argument('--url', type=str, required=True)
    parser_task.add_argument('--source', type=str)
    parser_task.add_argument('--name', type=str, required=True)
    parser_task.add_argument('--extension', type=str, required=True)

    args = parser.parse_args()

    if args.command == 'create_tables':
        create_all_tables()
    elif args.command == 'add_new_url':
        downloader = DatabaseSender(args.url, args.name, args.extension, args.source)
        downloader.create_record()
    else:
        parser.print_help()

