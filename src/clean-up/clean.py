import sys
from pathlib import Path

import snowflake.connector
from scripts import drop_db_script, drop_integration_script

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from config.settings import Settings

settings = Settings()


class Clean:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.connection = snowflake.connector.connect(
            user=self.settings.SNOWFLAKE_USER,
            password=self.settings.SNOWFLAKE_PASSWORD,
            account=self.settings.SNOWFLAKE_ACCOUNT,
        )

    def drop_database(self):
        """
        Pass
        """
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(drop_db_script)
            except Exception as e:
                print(e)

    def drop_integration(self):
        """
        Pass
        """
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(drop_integration_script)
            except Exception as e:
                print(e)

    def close_connection(self):
        self.connection.close()


if __name__ == "__main__":
    settings = Settings()
    clean = Clean(settings)
    try:
        clean.drop_database()
    except Exception as e:
        print(e)

    try:
        clean.drop_integration()
    except Exception as e:
        print(e)
    clean.close_connection()

    print("Successful clean")
