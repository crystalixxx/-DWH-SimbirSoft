import requests
import csv

from utils.database.core import DatabaseSender
from utils.prepare.converter import Converter
from utils.download.url import UrlHandler


class DownloadFile:
    def __init__(self, url: str, table_name: str, extension: str, resource: str):
        self.__url = url
        self.__table_name = table_name
        self.__extension = extension
        self.__resource = resource

    def download_csv(self):
        url_handler = UrlHandler(self.__url, self.__resource)

        data = requests.get(url_handler.hande_url())
        decoded_data = data.content.decode('utf-8')

        reader = csv.reader(decoded_data.splitlines(), delimiter=';', dialect='unix')

        heading = next(reader)

        rows = []
        for row in reader:
            rows.append(row)

        converter = Converter(heading, rows)
        columns_info = converter.validate_types()

        sender = DatabaseSender(self.__table_name, heading, rows, columns_info)
        sender.create_record()

    def download_json(self):
        pass

    def download(self):
        if self.__extension == 'csv':
            self.download_csv()
        elif self.__extension == 'json':
            self.download_json()
        else:
            raise Exception("Sorry, but we can't to process this file type now")

