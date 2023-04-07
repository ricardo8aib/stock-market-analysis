import sys
from pathlib import Path

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from config.settings import Settings

settings = Settings()

curated_view = f"""
    CREATE OR REPLACE VIEW
        {settings.DATABASE}.{settings.CURATED_SCHEMA}.{settings.CURATED_VIEW_NAME}
    AS
    SELECT *
    FROM
        {settings.DATABASE}.{settings.PREPARED_SCHEMA}.{settings.PREPARED_TABLE_NAME}
    ;
"""

grant_select = f"""
    GRANT SELECT
    ON VIEW {settings.DATABASE}.{settings.CURATED_SCHEMA}.{settings.CURATED_VIEW_NAME}
    TO ROLE {settings.READ_ROLE}
"""