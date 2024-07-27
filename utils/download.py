import requests
import re
import csv

from config import settings


def get_main_download_link(link):
    response = requests.get(link)
    page_content = response.text

    re_pattern = r'dispatcher.*?weblink_get.*?url":"(.*?)"'
    match = re.search(re_pattern, page_content)

    if match:
        url = match.group(1)
        parts = link.split('/')[-2:]
        url = f'{url}/{parts[0]}/{parts[1]}'
        return url

    return None


class DownloadFile:
    def __init__(self, url, file_name):
        self.__url = url
        self.__file_name = file_name

    def download_csv(self):
        data = requests.get(self.__url)
        decoded_data = data.content.decode('utf-8')

        reader = csv.reader(decoded_data.splitlines(), delimiter=';', dialect='unix')
        listed_reader = list(reader)

        with open(self.__file_name, "w") as file:
            for row in listed_reader:
                file.write(",".join(row) + '\n')

    def get_correct_downloader(self):
        extension = self.__file_name.split('.')[-1]

        if extension == 'csv':
            self.download_csv()
        else:
            raise Exception("Sorry, but we can't to process this file type now")


def download_file():
    downloader = DownloadFile(get_main_download_link(settings.DOWNLOAD_URL), settings.get_file_path())
    downloader.get_correct_downloader()

