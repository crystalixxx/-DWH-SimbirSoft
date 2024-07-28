import requests
import csv

from utils.database.core import DatabaseSender
from utils.prepare.converter import Converter


class DownloadFile:
    def __init__(self, url: str, table_name: str, extension: str):
        self.__url = url
        self.__table_name = table_name
        self.__extension = extension

    def download_csv(self):
        data = requests.get(self.__url)
        decoded_data = data.content.decode('utf-8')

        reader = csv.reader(decoded_data.splitlines(), delimiter=';', dialect='unix')

        heading = next(reader)

        rows = []
        for row in reader:
            rows.append(row)

        converter = Converter(heading, rows)
        columns_info = converter.validate_types()

        sender = DatabaseSender(self.__table_name, heading, rows, columns_info)
        sender.create_table()

    def download_json(self):
        pass

    def download(self):
        if self.__extension == 'csv':
            self.download_csv()
        elif self.__extension == 'json':
            self.download_json()
        else:
            raise Exception("Sorry, but we can't to process this file type now")

