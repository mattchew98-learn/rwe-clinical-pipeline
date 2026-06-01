"""Load the S3 Bronze files into Snowflake raw tables via COPY INTO."""
from __future__ import annotations

import snowflake.connector
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import TABLES, SnowflakeConfig
from .utils import get_logger

log = get_logger(__name__)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
def _connect(cfg: SnowflakeConfig):
    return snowflake.connector.connect(
        account=cfg.account,
        user=cfg.user,
        password=cfg.password,
        role=cfg.role,
        warehouse=cfg.warehouse,
        database=cfg.database,
        schema=cfg.schema,
    )


def copy_into_raw(cfg: SnowflakeConfig | None = None) -> None:
    """Run COPY INTO for every raw table from the external S3 stage."""
    cfg = cfg or SnowflakeConfig()
    if not (cfg.account and cfg.user and cfg.password):
        raise ValueError("Snowflake credentials are not fully set")
    conn = _connect(cfg)
    try:
        cur = conn.cursor()
        for filename, table in TABLES.items():
            sql = (
                f"COPY INTO {cfg.database}.{cfg.schema}.{table} "
                f"FROM @{cfg.database}.{cfg.schema}.{cfg.stage}/{filename} "
                "FILE_FORMAT = (TYPE = CSV SKIP_HEADER = 1 "
                "FIELD_OPTIONALLY_ENCLOSED_BY = '\"') ON_ERROR = 'CONTINUE'"
            )
            log.info("COPY INTO %s FROM %s", table, filename)
            cur.execute(sql)
    finally:
        conn.close()
    log.info("Snowflake load complete")
