class DatabaseSender:
    def __init__(self, table_name: str, header: list, raws: list, columns_info: dict):
        self.__table_name = table_name
        self.__header = header
        self.__raws = raws
        self.__columns_info = columns_info

    def create_record(self):
        print(f"Table with name {self.__table_name} created!")