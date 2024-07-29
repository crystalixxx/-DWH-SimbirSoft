import psycopg2

from utils.download.url import UrlHandler
from utils.download.download import DownloadFile
from utils.prepare.converter import Converter


def execute_script(query, params: tuple, is_returning: bool = False):
    try:
        with psycopg2.connect(dbname="postgres", host="localhost", user="admin", password="admin", port="5432") as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()

                if is_returning:
                    return cursor.fetchall()

    except psycopg2.Error as e:
        print(e)


class DatabaseSender:
    def __init__(self, url: str, resource: str, table_name: str, extension: str):
        self.__url = UrlHandler(url, resource).hande_url()
        self.__table_name = table_name
        self.__extension = extension
        self.__resource = resource

    def create_record(self):
        query = f"""
            INSERT INTO source(url, resource, table_name, extension)
            VALUES (%s, %s, %s, %s)
        """
        params = (self.__url, self.__resource, self.__table_name, self.__extension)

        execute_script(query, params)

    @staticmethod
    def get_all_records():
        return execute_script("SELECT * FROM source", (), True)


class TableHandler:
    def __init__(self, url: str, resource: str, table_name: str, extension: str):
        self.__url = url
        self.__resource = resource
        self.__table_name = table_name
        self.__extension = extension

        self.__heading, self.__rows = self.get_table_data()
        self.__columns_info = Converter(self.__heading, self.__rows).validate_types()

    def get_table_data(self):
        return DownloadFile(self.__url, self.__table_name, self.__extension, self.__resource).download()

    @staticmethod
    def get_creation_string(title: str, value: str, is_null: bool, is_pk: bool, is_last: bool):
        if is_pk:
            return f'\t"{title}" {"SERIAL" if value == "INTEGER" else value} PRIMARY KEY{"" if is_last else ","} \n'

        return f'\t"{title}" {value} {"NOT NULL" if is_null else ""}{"" if is_last else ","} \n'

    def table_create(self):
        sz = len(self.__columns_info)

        query = f"""CREATE TABLE IF NOT EXISTS {self.__table_name} ( \n"""
        for idx, column in self.__columns_info.items():
            value, is_null, is_pk = column
            query += self.get_creation_string(self.__heading[idx], value, is_null, is_pk, idx + 1 == sz)
        query += ")"

        execute_script(query, ())
        print(f"table {self.__table_name} created or existed early")

    def fill_data(self):
        query = f"""INSERT INTO {self.__table_name} ("""
        for idx, column in enumerate(self.__heading):
            query += f'"{column}" {", " if idx + 1 < len(self.__heading) else ""}'

        query += ') \n'
        query += 'VALUES '

        for idx, row in enumerate(self.__rows):
            sub_query = '('

            for sub_idx, value in enumerate(row):
                if self.__columns_info[sub_idx][0] == "VARCHAR":
                    sub_query += f"'{value}'{", " if sub_idx + 1 < len(row) else ""}"
                else:
                    if self.__columns_info[sub_idx][0] == "BOOLEAN":
                        sub_query += f'{bool(value)}{", " if sub_idx + 1 < len(row) else ""}'
                    else:
                        sub_query += f'{value}{", " if sub_idx + 1 < len(row) else ""}'

            sub_query += ')'
            query += sub_query + (", " if idx + 1 < len(self.__rows) else "")

        execute_script(query, ())


def create_all_tables():
    records = DatabaseSender.get_all_records()

    for record in records:
        idx, url, resource, table_name, extension = record

        handler = TableHandler(url, resource, table_name, extension)

        handler.table_create()
        handler.fill_data()
