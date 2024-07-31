from utils.download.url import UrlHandler
from utils.download.download import DownloadFile
from utils.prepare.converter import Converter

from .utils import execute_script

import logging
import tabulate


class DatabaseWorker:
    def __init__(self, url: str, resource: str, table_name: str, extension: str):
        self.__url = url
        self.__table_name = table_name
        self.__extension = extension
        self.__resource = resource

        try:
            self.__heading, self.__rows = DownloadFile(UrlHandler(url, resource).hande_url(), table_name, extension,
                                                       resource).download()
            self.__columns_info = Converter(self.__heading, self.__rows).validate_types()
            self.__ci_size = len(self.__columns_info)
        except Exception as e:
            logging.error(f"Во время инициализации инициализации класса произошла ошибка: {e}")
            raise e

    @staticmethod
    def get_all_records(show_data=False):
        logging.info(f"Просмотр всех данных таблицы source.")

        query = "SELECT * FROM source"

        try:
            data = execute_script(query, (), True)
            logging.info("Данные таблицы source успешно получены.")

            if not show_data:
                return data

            print(tabulate.tabulate(data, headers=["id", "url", "resource", "table_name", "extension"]))
        except Exception as e:
            logging.error(f"Ошибка по время получения данных таблицы source: {e}")

    def check_if_exists_table(self):
        query = f"""
        SELECT EXISTS (
            SELECT 1 FROM information_schema.tables 
            WHERE table_schema = 'public' 
            AND table_name = %s
        )
        """
        params = (self.__table_name,)

        try:
            logging.info(f"Проверка на существование таблицы {self.__table_name}")
            return execute_script(query, params, True)
        except Exception as e:
            logging.error(f"Ошибка во время проверки на существование таблицы {self.__table_name}: {e}")
            raise e

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
        query = f"""INSERT INTO "{self.__table_name}" ("""
        for idx, column in enumerate(self.__heading):
            query += f'"{column}"{self.get_endl_char(idx, len(self.__heading))}'

        query += ') \n'

        return query

    def create_record(self):
        if self.check_if_exists_table()[0][0]:
            print(f"Таблица с названием {self.__table_name} уже существует.")
            logging.info(f"Попытка добавления таблицы с уже существующим названием: {self.__table_name}.")
            return

        query = f"""
            INSERT INTO source(url, resource, table_name, extension)
            VALUES (%s, %s, %s, %s)
        """
        params = (self.__url, self.__resource, self.__table_name, self.__extension)

        try:
            execute_script(query, params)
            logging.info(f"Источник по ссылке {self.__url} был успешно добавлен")
            print(f"Источник данных по ссылке {self.__url} был успешно добавлен.")
        except Exception as e:
            logging.error(
                f"Обнаружена ошибка во время выполнения запроса на добавление источника по ссылке {self.__url}: {e}")

    @staticmethod
    def delete_record(idx=None, url=None, table_name=None):
        logging.info(f"Удаление источника с: id={idx}, url={url}, table_name={table_name}")

        data = execute_script("""
            SELECT id, table_name 
                FROM source s
            WHERE s.id = %s OR s.url = %s OR s.table_name = %s
        """, (idx, url, table_name), True)
        idx = data[0][0]
        table_name = data[0][1]

        query_delete_record = f"""
            DELETE FROM source s
            WHERE s.id = %s
        """
        params_delete_record = (idx,)

        try:
            execute_script(query_delete_record, params_delete_record)
            logging.info(f"Удален источник с: id={idx}, url={url}, table_name={table_name}")
            print(f"Удален источник с: id={idx}, url={url}, table_name={table_name}")

            try:
                query_delete_table = f"""
                    DROP TABLE "{table_name}"
                """

                execute_script(query_delete_table, ())
                logging.info(f"Удалена таблица {table_name}.")
                print(f"Удалена таблица {table_name}")
            except Exception as e:
                pass

        except Exception as e:
            logging.error(f"Ошибка во время удаления источника (id={idx}, url={url}, table_name={table_name}): {e}")

    def table_create(self):
        exists_later = self.check_if_exists_table()[0][0]

        query = f"""CREATE TABLE IF NOT EXISTS "{self.__table_name}" ( \n"""
        for idx, column in self.__columns_info.items():
            value, is_null, is_pk = column
            query += self.get_creation_string(self.__heading[idx], value, is_null, is_pk, idx + 1 == self.__ci_size)
        query += ")"

        try:
            execute_script(query, ())
            logging.info(f"Таблица {self.__table_name} была успешно создана.")

            if not exists_later:
                self.fill_data()
        except Exception as e:
            logging.error(
                f"Ошибка во время создания таблицы {self.__table_name} из источника по ссылке {self.__url}: {e}")

    def fill_data(self):
        query = self.get_insert_title() + self.get_insert_string()

        try:
            execute_script(query, ())
            logging.info(f"Вставка данных для таблицы {self.__table_name} произведена успешно.")
        except Exception as e:
            logging.error(f"Проблема во время добавления данных в таблицу {self.__table_name}: {e}")
            raise e


def create_all_tables():
    records = DatabaseWorker.get_all_records()

    for record in records:
        idx, url, resource, table_name, extension = record
        handler = DatabaseWorker(url, resource, table_name, extension)

        handler.table_create()
        print(f"Таблица {table_name} была успешно обработана.")
