import sys
from pathlib import Path

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from config.settings import Settings  # noqa: E402

settings = Settings()

curated_view = f"""
    CREATE OR REPLACE VIEW
        {settings.DATABASE}.{settings.CURATED_SCHEMA}.{settings.CURATED_VIEW_NAME}
    AS
    SELECT
        DISTINCT *
    FROM
        {settings.DATABASE}.{settings.PREPARED_SCHEMA}.{settings.PREPARED_TABLE_NAME}
    ;
"""
