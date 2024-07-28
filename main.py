from utils.download.download import DownloadFile
from utils.parse import Parser
from utils.prepare.converter import Converter

from argparse import ArgumentParser

if __name__ == '__main__':
    parser = ArgumentParser()
    subparsers = parser.add_subparsers(dest='command')

    parse_create = subparsers.add_parser('create_table')

    parser_task = subparsers.add_parser('add_new_url')
    parser_task.add_argument('--url', type=str, required=True)
    parser_task.add_argument('--source', type=str)
    parser_task.add_argument('--name', type=str, required=True)
    parser_task.add_argument('--extension', type=str, required=True)

    args = parser.parse_args()

    if args.command == 'create_table':
        print("tables created")
    elif args.command == 'add_new_url':
        downloader = DownloadFile(args.url, args.name, args.extension, args.source)
        downloader.download_csv()

        # print(f"url: {args.url}")
        # print(f"source: {args.source}")
        # print(f"name: {args.name}")
        # print(f"extension: {args.extension}")
    else:
        parser.print_help()

