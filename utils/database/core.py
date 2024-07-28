import psycopg2


class DatabaseSender:
    def __init__(self, record_data: tuple, header: list, raws: list, columns_info: dict):
        self.__record_data = record_data
        self.__header = header
        self.__raws = raws
        self.__columns_info = columns_info

    def create_record(self):
        try:
            with psycopg2.connect(dbname="postgres", host="localhost", user="admin", password="admin", port="5432") as conn:
                with conn.cursor() as cursor:
                    query = f"""
                        INSERT INTO source(url, resource, table_name, extension)
                        VALUES (%s, %s, %s, %s)
                    """

                    cursor.execute(query, self.__record_data)
                    conn.commit()

                    print(f"Table with name {self.__record_data[2]} created")
        except Exception as e:
            print(e)
