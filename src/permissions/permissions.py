import sys
from pathlib import Path

import snowflake.connector
from scripts import grant_db, grant_schema, grant_view

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from config.settings import Settings

settings = Settings()


class Permissions:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.connection = snowflake.connector.connect(
            user=self.settings.SNOWFLAKE_USER,
            password=self.settings.SNOWFLAKE_PASSWORD,
            account=self.settings.SNOWFLAKE_ACCOUNT,
        )

    def grant_permissions(self):
        """
        Pass
        """
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(grant_db)
                cursor.execute(grant_schema)
                cursor.execute(grant_view)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    settings = Settings()
    permissions = Permissions(settings)
    permissions.grant_permissions()
