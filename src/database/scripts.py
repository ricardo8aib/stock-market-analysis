import sys
from pathlib import Path

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from config.settings import Settings  # noqa: E402

settings = Settings()

# Create Database
database = f"""
        CREATE DATABASE {settings.DATABASE};
    """

# Create Schemas
landing_schema = f"""
        CREATE SCHEMA {settings.DATABASE}.{settings.LANDING_SCHEMA};
    """

raw_schema = f"""
        CREATE SCHEMA {settings.DATABASE}.{settings.RAW_SCHEMA};
    """

prepared_schema = f"""
        CREATE SCHEMA {settings.DATABASE}.{settings.PREPARED_SCHEMA};
    """

curated_schema = f"""
        CREATE SCHEMA {settings.DATABASE}.{settings.CURATED_SCHEMA};
    """

# Create file format
file_format = f"""
        CREATE OR REPLACE FILE FORMAT
            {settings.DATABASE}.{settings.LANDING_SCHEMA}.{settings.LANDING_FILE_FORMAT}
        TYPE = JSON
        ;
    """
