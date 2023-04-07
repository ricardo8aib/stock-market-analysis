import sys
from pathlib import Path

import pandas as pd
import snowflake.connector
from scripts import (
    desc_storage_integration,
    landing_table,
    prepared_table,
    raw_table,
    stage,
    storage_integration,
)

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from config.settings import Settings

settings = Settings()


class Ingestion:
    def __init__(self, settings: Settings):
        self.settings = settings
        self.connection = snowflake.connector.connect(
            user=self.settings.SNOWFLAKE_USER,
            password=self.settings.SNOWFLAKE_PASSWORD,
            account=self.settings.SNOWFLAKE_ACCOUNT,
        )

    def create_storage_integration(self):
        """
        Pass
        """
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(storage_integration)
            except Exception as e:
                print(e)

    def create_stage(self):
        """
        Pass
        """
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(stage)
            except Exception as e:
                print(e)

    def create_tables(self):
        """
        Pass
        """
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(landing_table)
                cursor.execute(raw_table)
                cursor.execute(prepared_table)
            except Exception as e:
                print(e)

    def show_integration_data(self):
        """
        Pass
        """
        with self.connection.cursor() as cursor:
            try:
                cursor.execute(desc_storage_integration)
                data = cursor.fetchall()
                result = pd.DataFrame(data)
                result.set_index(0, inplace=True)
                iam_user_arn = result.loc["STORAGE_AWS_IAM_USER_ARN", 2]
                external_id = result.loc["STORAGE_AWS_EXTERNAL_ID", 2]

                print(
                    f"""
                    Add the STORAGE_AWS_IAM_USER_ARN: {iam_user_arn},
                    and the STORAGE_AWS_EXTERNAL_ID: {external_id} to the
                    Trust Relationship Policy of the following IAM Role:
                    {settings.S3_ROLE}
                """
                )

            except Exception as e:
                print(e)

    def close_connection(self):
        self.connection.close()


if __name__ == "__main__":
    settings = Settings()
    ingestion = Ingestion(settings)
    ingestion.create_storage_integration()
    ingestion.create_stage()
    ingestion.create_tables()
    ingestion.show_integration_data()
    ingestion.close_connection()
