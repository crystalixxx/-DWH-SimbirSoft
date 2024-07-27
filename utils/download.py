import requests
import re
import csv

from config import settings


class DownloadFile:
    __url = settings.get_url()
    __file_name = settings.get_file_path()

    @staticmethod
    def download_csv():
        data = requests.get(DownloadFile.__url)
        decoded_data = data.content.decode('utf-8')

        reader = csv.reader(decoded_data.splitlines(), delimiter=';', dialect='unix')
        listed_reader = list(reader)

        with open(DownloadFile.__file_name, "w") as file:
            for row in listed_reader:
                file.write(",".join(row) + '\n')

    @staticmethod
    def download_json():
        pass

    @staticmethod
    def download():
        extension = DownloadFile.__file_name.split('.')[-1]

        if extension == 'csv':
            DownloadFile.download_csv()
        elif extension == 'json':
            DownloadFile.download_json()
        else:
            raise Exception("Sorry, but we can't to process this file type now")

