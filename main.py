from utils.database.core import DatabaseWorker, create_all_tables

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
        downloader = DatabaseWorker(args.url, args.source, args.name, args.extension)
        downloader.create_record()
    else:
        parser.print_help()


# from utils.database.core import DatabaseWorker, create_all_tables
#
# if __name__ == '__main__':
#     while True:
#         commands = input().split()
#
#         if commands[0] == 'create_tables':
#             create_all_tables()
#         elif commands[0] == 'add_new_url':
#             url, resource, name, extension = commands[1:]
#             downloader = DatabaseWorker(url, resource, name, extension)
#             downloader.create_record()
#         else:
#             print("""
#             Invalid command. You can use only:
#             - create_tables
#             - add_new_url <url> <resource> <table_name> <extension>
#             """)
#
