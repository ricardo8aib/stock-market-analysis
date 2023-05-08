import sys
from pathlib import Path

path_root = Path(__file__).parents[1]
sys.path.append(str(path_root))

from config.settings import Settings  # noqa: E402

settings = Settings()

landing_task = f"""
    CREATE OR REPLACE TASK
        {settings.DATABASE}.{settings.LANDING_SCHEMA}.{settings.LANDING_TASK}
    WAREHOUSE={settings.WAREHOUSE}
    SCHEDULE='{settings.LANDING_TASK_SCHEDULE}'
    AS
    INSERT INTO {settings.DATABASE}.{settings.LANDING_SCHEMA}.{settings.LANDIGN_TABLE_NAME} (
        RAW,
        STAGE_FILE_NAME,
        LOAD_TS
    )
    SELECT
        T.$1 AS RAW,
        METADATA$FILENAME AS STAGE_FILE_NAME,
        CURRENT_TIMESTAMP() AS LOAD_TS
    FROM
        @{settings.DATABASE}.{settings.LANDING_SCHEMA}.{settings.STAGE_NAME}/{settings.STAGE_FOLDER}
    (FILE_FORMAT => '{settings.DATABASE}.{settings.LANDING_SCHEMA}.{settings.LANDING_FILE_FORMAT}')
    AS T
    WHERE TO_TIMESTAMP(T.$1:_airbyte_data::variant:t::integer/1000) > COALESCE((
        SELECT
            TO_TIMESTAMP(MAX(RAW:_airbyte_data::variant:t::integer/1000))
        FROM {settings.DATABASE}.{settings.LANDING_SCHEMA}.{settings.LANDIGN_TABLE_NAME}
    ), '1900-01-01')
    ;
"""

raw_task = f"""
    CREATE OR REPLACE TASK {settings.DATABASE}.{settings.LANDING_SCHEMA}.{settings.RAW_TASK}
    WAREHOUSE={settings.WAREHOUSE}
    AFTER {settings.DATABASE}.{settings.LANDING_SCHEMA}.{settings.LANDING_TASK}
    AS
    INSERT INTO {settings.DATABASE}.{settings.RAW_SCHEMA}.{settings.RAW_TABLE_NAME} (
        AIRBYTE_AB_ID,
        AIRBYTE_EMITTED_AT,
        SYMBOL,
        V,
        VW,
        O,
        C,
        H,
        L,
        T,
        N,
        STAGE_FILE_NAME,
        LOAD_TS
    )
    SELECT
        RAW:_airbyte_ab_id::varchar,
        RAW:_airbyte_emitted_at::integer,
        TO_VARCHAR(SPLIT(STAGE_FILE_NAME, '/')[1]),
        RAW:_airbyte_data::variant:v::float,
        RAW:_airbyte_data::variant:vw::float,
        RAW:_airbyte_data::variant:o::float,
        RAW:_airbyte_data::variant:c::float,
        RAW:_airbyte_data::variant:h::float,
        RAW:_airbyte_data::variant:l::float,
        RAW:_airbyte_data::variant:t::integer,
        RAW:_airbyte_data::variant:n::integer,
        STAGE_FILE_NAME,
        LOAD_TS AS LOAD_TS
    FROM {settings.DATABASE}.{settings.LANDING_SCHEMA}.{settings.LANDIGN_TABLE_NAME}
    WHERE TO_TIMESTAMP(RAW:_airbyte_data::variant:t::integer/1000) > COALESCE((
        SELECT
            TO_TIMESTAMP(MAX(T/1000))
        FROM {settings.DATABASE}.{settings.RAW_SCHEMA}.{settings.RAW_TABLE_NAME}
    ), '1900-01-01')
    ;
"""

prepared_task = f"""
    CREATE OR REPLACE TASK {settings.DATABASE}.{settings.LANDING_SCHEMA}.{settings.PREPARED_TASK}
    WAREHOUSE={settings.WAREHOUSE}
    AFTER {settings.DATABASE}.{settings.LANDING_SCHEMA}.{settings.RAW_TASK}
    AS
    INSERT INTO {settings.DATABASE}.{settings.PREPARED_SCHEMA}.{settings.PREPARED_TABLE_NAME} (
        SYMBOL,
        VOLUME,
        VOLUMEWEIGHTED,
        OPEN,
        CLOSE,
        HIGHEST,
        LOWEST,
        DATE,
        NTRANSACTIONS,
        STAGE_FILE_NAME,
        LOAD_TS
    )
    SELECT
        SYMBOL,
        V,
        VW,
        O,
        C,
        H,
        L,
        TO_DATE(TO_TIMESTAMP(T/1000)),
        N,
        STAGE_FILE_NAME,
        LOAD_TS
    FROM {settings.DATABASE}.{settings.RAW_SCHEMA}.{settings.RAW_TABLE_NAME}
    WHERE TO_TIMESTAMP(T/1000) > COALESCE((
        SELECT
            MAX(DATE)
        FROM {settings.DATABASE}.{settings.PREPARED_SCHEMA}.{settings.PREPARED_TABLE_NAME}
    ), '1900-01-01')
    ;
"""

resume_landing = f"""
    ALTER TASK
    {settings.DATABASE}.{settings.LANDING_SCHEMA}.{settings.LANDING_TASK}
    RESUME
"""

resume_raw = f"""
    ALTER TASK
    {settings.DATABASE}.{settings.LANDING_SCHEMA}.{settings.RAW_TASK}
    RESUME
"""

resume_prepared = f"""
    ALTER TASK
    {settings.DATABASE}.{settings.LANDING_SCHEMA}.{settings.PREPARED_TASK}
    RESUME
"""
