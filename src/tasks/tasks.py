import sys
from pathlib import Path

import snowflake.connector
from scripts import (
    landing_task,
    prepared_task,
    raw_task,
    resume_landing,
    resume_prepared,
    resume_raw,
)

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from config.settings import Settings  # noqa: E402

settings = Settings()


class Tasks:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.connection = snowflake.connector.connect(
            user=self.settings.SNOWFLAKE_USER,
            password=self.settings.SNOWFLAKE_PASSWORD,
            account=self.settings.SNOWFLAKE_ACCOUNT,
        )

    def create_tasks(self):
        """
        Pass
        """
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(landing_task)
                cursor.execute(raw_task)
                cursor.execute(prepared_task)
            except Exception as e:
                print(e)

    def resume_tasks(self):
        """ """
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(resume_prepared)
                cursor.execute(resume_raw)
                cursor.execute(resume_landing)
            except Exception as e:
                print(e)

    def close_connection(self):
        self.connection.close()


if __name__ == "__main__":
    settings = Settings()
    tasks = Tasks(settings)
    tasks.create_tasks()
    tasks.resume_tasks()
    tasks.close_connection()
