import sys
from pathlib import Path

import snowflake.connector
from scripts import curated_view, grant_select

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from config.settings import Settings

settings = Settings()


class Views:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.connection = snowflake.connector.connect(
            user=self.settings.SNOWFLAKE_USER,
            password=self.settings.SNOWFLAKE_PASSWORD,
            account=self.settings.SNOWFLAKE_ACCOUNT,
        )

    def create_view(self):
        """
        Pass
        """
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(curated_view)
            except Exception as e:
                print(e)

    def grant_select_permissions(self):
        """
        Pass
        """
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(grant_select)
            except Exception as e:
                print(e)


if __name__ == "__main__":
    settings = Settings()
    views = Views(settings)
    views.create_view()
    views.grant_select_permissions()
