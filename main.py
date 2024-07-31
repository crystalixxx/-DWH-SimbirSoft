from utils.database.core import DatabaseWorker, create_all_tables

from argparse import ArgumentParser
import logging
from datetime import datetime

if __name__ == '__main__':
    cur_date = datetime.strftime(datetime.now(), "%Y_%m_%d_%H_%M_%S")

    logging.basicConfig(
        level=logging.INFO,
        filename=f"logs/all_logs.log",
        filemode="a",
        format="%(asctime)s %(levelname)s %(message)s"
    )

    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    parse_create = subparsers.add_parser('create_tables')

    parser_task = subparsers.add_parser('add_new_url')
    parser_task.add_argument('--url', type=str, required=True)
    parser_task.add_argument('--source', type=str)
    parser_task.add_argument('--name', type=str, required=True)
    parser_task.add_argument('--extension', type=str, required=True)

    parser_all_tasks = subparsers.add_parser('all_files')

    parser_deleter = subparsers.add_parser('delete_url')
    parser_deleter.add_argument('--id', type=str)
    parser_deleter.add_argument('--url', type=str)
    parser_deleter.add_argument('--table_name', type=str)

    args = parser.parse_args()

    if args.command == 'create_tables':
        logging.info("Начался процесс создания всех таблиц.")
        create_all_tables()
    else:
        try:
            if args.command == 'add_new_url':
                downloader = DatabaseWorker(args.url, args.source, args.name, args.extension)
                downloader.create_record()
            elif args.command == "all_files":
                DatabaseWorker.get_all_records(True)
            elif args.command == "delete_url":
                if args.id is None and args.url is None and args.table_name is None:
                    parser.print_help()
                else:
                    DatabaseWorker.delete_record(args.id, args.url, args.table_name)
            else:
                parser.print_help()
        except Exception as e:
            print(f"Во время исполнения произошла ошибка: {e}. Убедитесь в корректности введенных данных.")


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
