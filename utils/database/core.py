from utils.download.url import UrlHandler
from utils.download.download import DownloadFile
from utils.prepare.converter import Converter

from .utils import execute_script


class DatabaseWorker:
    def __init__(self, url: str, resource: str, table_name: str, extension: str):
        self.__url = url
        self.__table_name = table_name
        self.__extension = extension
        self.__resource = resource

        self.__heading, self.__rows = DownloadFile(UrlHandler(url, resource).hande_url(), table_name, extension,
                                                   resource).download()
        self.__columns_info = Converter(self.__heading, self.__rows).validate_types()
        self.__ci_size = len(self.__columns_info)

    @staticmethod
    def get_all_records():
        return execute_script("SELECT * FROM source", (), True)

    @staticmethod
    def get_creation_string(title: str, value: str, is_null: bool, is_pk: bool, is_last: bool):
        if is_pk:
            return f'\t"{title}" {"SERIAL" if value == "INTEGER" else value} PRIMARY KEY{"" if is_last else ","} \n'

        return f'\t"{title}" {value} {"NOT NULL" if is_null else ""}{"" if is_last else ","} \n'

    @staticmethod
    def get_endl_char(idx, length):
        if idx + 1 == length:
            return ""

        return ", "

    def get_insert_string(self):
        query = 'VALUES '

        for idx, row in enumerate(self.__rows):
            sub_query = '('

            for sub_idx, value in enumerate(row):
                sub_query += f'{value}{self.get_endl_char(sub_idx, len(row))}'

            sub_query += ')'
            query += sub_query + self.get_endl_char(idx, len(self.__rows))

        return query

    def get_insert_title(self):
        query = f"""INSERT INTO {self.__table_name} ("""
        for idx, column in enumerate(self.__heading):
            query += f'"{column}" {", " if idx + 1 < len(self.__heading) else ""}'

        query += ') \n'

        return query

    def create_record(self):
        query = f"""
            INSERT INTO source(url, resource, table_name, extension)
            VALUES (%s, %s, %s, %s)
        """
        params = (self.__url, self.__resource, self.__table_name, self.__extension)

        execute_script(query, params)

    def table_create(self):
        query = f"""CREATE TABLE IF NOT EXISTS {self.__table_name} ( \n"""
        for idx, column in self.__columns_info.items():
            value, is_null, is_pk = column
            query += self.get_creation_string(self.__heading[idx], value, is_null, is_pk, idx + 1 == self.__ci_size)
        query += ")"

        execute_script(query, ())
        print(f"table {self.__table_name} created or existed early")

    def fill_data(self):
        query = self.get_insert_title() + self.get_insert_string()

        execute_script(query, ())


def create_all_tables():
    records = DatabaseWorker.get_all_records()

    for record in records:
        idx, url, resource, table_name, extension = record
        handler = DatabaseWorker(url, resource, table_name, extension)

        handler.table_create()
        handler.fill_data()
