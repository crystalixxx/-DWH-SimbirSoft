# todo: Реализовать класс / функции для определения типа данных столбца + выделения из всех столбцов primary_key,
#  если такое возможно

from .validation import *

from collections import defaultdict


class Converter:
    def __init__(self, heading, rows):
        self.__heading = heading.copy()
        self.__rows = rows.copy()

        self.__types = defaultdict(tuple)
        self.__columns = [[] for _ in range(len(self.__heading))]

        self.__validate_functions = {
            is_bool_column: "BOOLEAN",
            is_int_column: "INT",
            is_float_column: "DECIMAL",
            is_datetime_column: "TIMESTAMP",
            is_str_column: "VARCHAR"
        }

        self.convert_types()
        self.fill_columns()

    def fill_columns(self):
        for i in range(len(self.__heading)):
            for j in range(len(self.__rows)):
                self.__columns[i].append(self.__rows[j][i])

    def convert_types(self):
        convert_types = [int, float, str]

        for i in range(len(self.__rows)):
            for j in range(len(self.__columns)):
                for type_ in convert_types:
                    try:
                        self.__rows[i][j] = type_(self.__rows[i][j])
                        break
                    except ValueError:
                        continue

    def validate_types(self):
        primary_key = None
        for idx, column in enumerate(self.__columns):
            value, is_null, is_unique = None, can_be_nullable(column), is_unique_column(column)

            for callback, type_ in self.__validate_functions.items():
                if callback(column):
                    value = type_
                    break

            self.__types[idx] = (value, is_null, is_unique)

            if (primary_key is None) and (not is_null) and is_unique:
                primary_key = idx

        return self.__types
