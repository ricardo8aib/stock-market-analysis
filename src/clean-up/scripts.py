import sys
from pathlib import Path

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from config.settings import Settings

settings = Settings()

# Drop Database
drop_db_script = f"""
        DROP DATABASE {settings.DATABASE};
    """

# Drop integration
drop_integration_script = f"""
        DROP STORAGE INTEGRATION {settings.STORAGE_INTEGRATION};
    """
