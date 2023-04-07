import sys
from pathlib import Path

import snowflake.connector
from scripts import (
    curated_schema,
    database,
    file_format,
    landing_schema,
    prepared_schema,
    raw_schema,
)

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from config.settings import Settings

settings = Settings()


class DataBase:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.connection = snowflake.connector.connect(
            user=self.settings.SNOWFLAKE_USER,
            password=self.settings.SNOWFLAKE_PASSWORD,
            account=self.settings.SNOWFLAKE_ACCOUNT,
        )

    def create_database(self):
        """
        Pass
        """
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(database)
            except Exception as e:
                print(e)

    def create_schemas(self):
        """
        Pass
        """
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(landing_schema)
                cursor.execute(raw_schema)
                cursor.execute(prepared_schema)
                cursor.execute(curated_schema)
            except Exception as e:
                print(e)

    def create_file_format(self):
        """ """
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(file_format)
            except Exception as e:
                print(e)

    def close_connection(self):
        self.connection.close()


if __name__ == "__main__":
    settings = Settings()
    db = DataBase(settings)
    db.create_database()
    db.create_schemas()
    db.create_file_format()
    db.close_connection()
