import os

import pydantic


class Settings(pydantic.BaseSettings):
    # Aws Settings
    BUCKET_NAME: str
    STAGE_FOLDER: str
    AWS_ACCOUNT_ID: str
    S3_ROLE: str
    READ_ROLE: str

    # Snowflake Settings
    # Generals
    DATABASE: str
    STORAGE_INTEGRATION: str
    STAGE_NAME: str
    LANDING_FILE_FORMAT: str
    WAREHOUSE: str
    # Schemas
    LANDING_SCHEMA: str
    RAW_SCHEMA: str
    PREPARED_SCHEMA: str
    CURATED_SCHEMA: str
    # Auth info
    SNOWFLAKE_USER: str
    SNOWFLAKE_PASSWORD: str
    SNOWFLAKE_ACCOUNT: str
    # Table names
    LANDIGN_TABLE_NAME: str
    RAW_TABLE_NAME: str
    PREPARED_TABLE_NAME: str
    CURATED_VIEW_NAME: str
    PREPARED_FORECAST_TABLE_NAME: str
    CURATED_FORECAST_VIEW_NAME: str
    CURATED_FORECAST_METRICS_VIEW_NAME: str
    # Tasks
    LANDING_TASK_SCHEDULE: str
    LANDING_TASK: str
    RAW_TASK: str
    PREPARED_TASK: str

    class Config:
        env_file = os.path.join(os.path.dirname(__file__), "..", "..", ".env")
        env_file_encoding = "utf-8"
