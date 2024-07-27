import csv

from config import settings


class Parser:
    working_file: str = settings.get_file_path()

    @classmethod
    def parse_csv(cls: "Parser"):
        columns = []
        rows = []

        with open(cls.working_file, 'r') as file:
            reader = csv.reader(file, delimiter=',')

            columns = next(reader)

            for row in reader:
                rows.append(row)

        return columns, rows

    @classmethod
    def parse_json(cls: "Parser"):
        pass

    @classmethod
    def parse(cls: "Parser"):
        extension = cls.working_file.split('.')[-1]

        if extension == 'csv':
            return cls.parse_csv()
        elif extension == 'json':
            return cls.parse_json()
        else:
            raise Exception("Sorry, we can't to parse this file type now")
