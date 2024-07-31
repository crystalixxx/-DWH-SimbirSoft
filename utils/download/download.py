import requests
import csv
import logging


class DownloadFile:
    def __init__(self, url: str, table_name: str, extension: str, resource: str):
        self.__url = url
        self.__table_name = table_name
        self.__extension = extension
        self.__resource = resource

    def download_csv(self):
        data = requests.get(self.__url)
        decoded_data = data.content.decode('utf-8')

        reader = csv.reader(decoded_data.splitlines(), delimiter=';', dialect='unix')
        heading = next(reader)

        rows = []
        for row in reader:
            rows.append(row)

        return heading, rows

    def download_json(self):
        try:
            request = requests.get(self.__url)
            if request.status_code != 200:
                logging.error(f"Произошла ошибка при скачивании файла для таблицы {self.__table_name}.")
                raise Exception

            data = request.json()
            heading = ["id"]
            rows = [[] for _ in range(len(data))]

            for idx, value in enumerate(data.keys()):
                rows[idx].append(value)

            for idx, value in enumerate(data.values()):
                for key, item in value.items():
                    if idx < 1:
                        heading.append(key)

                    rows[idx].append(item)

            return heading, rows

        except Exception as e:
            logging.error(
                f"Ошибка при скачивании JSON файла: {e}. Убедитесь в том, что расширение файла в действительности JSON.")
            raise Exception(e)

    def download(self):
        if self.__extension == 'csv':
            return self.download_csv()
        elif self.__extension == 'json':
            return self.download_json()
        else:
            raise Exception(f"На данный момент не может обработать файл с расширением {self.__extension}")
