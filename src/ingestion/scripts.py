import sys
from pathlib import Path

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from config.settings import Settings

settings = Settings()

storage_integration = f"""
        CREATE OR REPLACE STORAGE INTEGRATION {settings.STORAGE_INTEGRATION}
            TYPE = EXTERNAL_STAGE
            STORAGE_PROVIDER = S3
            ENABLED = TRUE
            STORAGE_AWS_ROLE_ARN = 'arn:aws:iam::{settings.AWS_ACCOUNT_ID}:role/{settings.S3_ROLE}'
            STORAGE_ALLOWED_LOCATIONS = ('s3://{settings.BUCKET_NAME}');
    """

stage = f"""
        CREATE OR REPLACE STAGE {settings.DATABASE}.{settings.LANDING_SCHEMA}.{settings.STAGE_NAME}
        url = ('s3://{settings.BUCKET_NAME}/')
        storage_integration = {settings.STORAGE_INTEGRATION};
    """

# Ingestion tables
landing_table = f"""
        CREATE OR REPLACE TABLE
        {settings.DATABASE}.{settings.LANDING_SCHEMA}.{settings.LANDIGN_TABLE_NAME}(
            RAW VARIANT,
            STAGE_FILE_NAME VARCHAR(16777216),
            LOAD_TS TIMESTAMP_NTZ(9)
        )
        ;
    """

raw_table = f"""
        CREATE OR REPLACE TABLE
        {settings.DATABASE}.{settings.RAW_SCHEMA}.{settings.RAW_TABLE_NAME}(
            AIRBYTE_AB_ID VARCHAR(16777216),
            AIRBYTE_EMITTED_AT NUMBER(30, 0),
            SYMBOL VARCHAR(200),
            V NUMBER(30, 2),
            VW NUMBER(30, 4),
            O NUMBER(30, 2),
            C NUMBER(30, 2),
            H NUMBER(30, 2),
            L NUMBER(30, 2),
            T NUMBER(30, 0),
            N NUMBER(30, 0),
            STAGE_FILE_NAME VARCHAR(16777216),
            LOAD_TS TIMESTAMP_NTZ(9)
        )
        ;
    """

prepared_table = f"""
        CREATE OR REPLACE TABLE
        {settings.DATABASE}.{settings.PREPARED_SCHEMA}.{settings.PREPARED_TABLE_NAME}(
            SYMBOL VARCHAR(200),
            VOLUME NUMBER(30, 2),
            VOLUMEWEIGHTED NUMBER(30, 4),
            OPEN NUMBER(30, 2),
            CLOSE NUMBER(30, 2),
            HIGHEST NUMBER(30, 2),
            LOWEST NUMBER(30, 2),
            DATE DATE,
            NTRANSACTIONS NUMBER(30, 0),
            STAGE_FILE_NAME VARCHAR(16777216),
            LOAD_TS TIMESTAMP_NTZ(9)
        )
        ;
    """

desc_storage_integration = f"""
       DESC INTEGRATION {settings.STORAGE_INTEGRATION};
    """
