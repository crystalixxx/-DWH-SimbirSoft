import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

DB_NAME = os.getenv('DB_NAME')
DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_PORT = os.getenv('DB_PORT')


def execute_script(query, params: tuple, is_returning: bool = False):
    try:
        with psycopg2.connect(dbname=DB_NAME, host=DB_HOST, user=DB_USER, password=DB_PASS, port=DB_PORT) as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()

                if is_returning:
                    return cursor.fetchall()

    except psycopg2.Error as e:
        print(e)
