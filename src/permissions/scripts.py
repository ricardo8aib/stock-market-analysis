import sys
from pathlib import Path

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from config.settings import Settings

settings = Settings()

grant_db = f"""
    GRANT USAGE
    ON DATABASE {settings.DATABASE}
    TO ROLE {settings.READ_ROLE}
    ;
"""

grant_schema = f"""
    GRANT USAGE
    ON SCHEMA {settings.DATABASE}.{settings.CURATED_SCHEMA}
    TO ROLE {settings.READ_ROLE}
"""

grant_view = f"""
    GRANT SELECT
    ON VIEW {settings.DATABASE}.{settings.CURATED_SCHEMA}.{settings.CURATED_VIEW_NAME}
    TO ROLE {settings.READ_ROLE}
"""
