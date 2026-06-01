"""Central configuration, read from environment variables.

Local dev: export these (or put them in a .env file — see .env.example).
CI / production: provide them as GitHub Actions secrets.
"""
from __future__ import annotations

import os
from dataclasses import dataclass

# Where Synthea wrote its CSVs (default matches the Synthea ./output/csv folder)
SYNTHEA_CSV_DIR = os.getenv("SYNTHEA_CSV_DIR", "output/csv")

# Maps each Synthea CSV file -> its Snowflake raw table name
TABLES: dict[str, str] = {
    "patients.csv": "patients",
    "conditions.csv": "conditions",
    "procedures.csv": "procedures",
    "medications.csv": "medications",
    "encounters.csv": "encounters",
}


@dataclass(frozen=True)
class S3Config:
    bucket: str = os.getenv("S3_BUCKET", "")
    prefix: str = os.getenv("S3_PREFIX", "bronze")


@dataclass(frozen=True)
class SnowflakeConfig:
    account: str = os.getenv("SNOWFLAKE_ACCOUNT", "")
    user: str = os.getenv("SNOWFLAKE_USER", "")
    password: str = os.getenv("SNOWFLAKE_PASSWORD", "")
    role: str = os.getenv("SNOWFLAKE_ROLE", "SYSADMIN")
    warehouse: str = os.getenv("SNOWFLAKE_WAREHOUSE", "WH_DEV")
    database: str = os.getenv("SNOWFLAKE_DATABASE", "RWE")
    schema: str = os.getenv("SNOWFLAKE_SCHEMA", "RAW")
    stage: str = os.getenv("SNOWFLAKE_STAGE", "S3_BRONZE")
