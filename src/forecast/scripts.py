import sys
from pathlib import Path

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from config.settings import Settings

settings = Settings()

select_all = f"""
        SELECT
            *
        FROM {settings.DATABASE}.{settings.CURATED_SCHEMA}.{settings.CURATED_VIEW_NAME}
        ;
    """

create_forecast_table = f"""
        CREATE OR REPLACE TABLE
        {settings.DATABASE}.{settings.PREPARED_SCHEMA}.{settings.PREPARED_FORECAST_TABLE_NAME}(
            DATE VARCHAR,
            FORECAST FLOAT,
            MSE FLOAT,
            RMSE FLOAT,
            MAPE FLOAT,
            MAE FLOAT,
            METHOD VARCHAR(50),
            SYMBOL VARCHAR(50)
        )
        ;
    """

curated_forecast_view = f"""
    CREATE OR REPLACE VIEW
        {settings.DATABASE}.{settings.CURATED_SCHEMA}.{settings.CURATED_FORECAST_VIEW_NAME}
    AS
    SELECT
        TO_DATE(TO_TIMESTAMP(TO_NUMBER(DATE)/1000000)) AS DATE,
        FORECAST,
        MSE,
        RMSE,
        MAPE,
        MAE,
        METHOD,
        SYMBOL
    FROM
        {settings.DATABASE}.{settings.PREPARED_SCHEMA}.{settings.PREPARED_FORECAST_TABLE_NAME}
    ;
"""

grant_forecast_view = f"""
    GRANT SELECT
    ON VIEW {settings.DATABASE}.{settings.CURATED_SCHEMA}.{settings.CURATED_FORECAST_VIEW_NAME}
    TO ROLE {settings.READ_ROLE}
"""
