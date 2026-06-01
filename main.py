"""End-to-end entrypoint: extract (locate) -> S3 Bronze -> Snowflake raw.

    python main.py

Then transform with dbt:

    cd dbt/rwe_dbt && dbt build
"""
from __future__ import annotations

import sys

from pipeline.extract import find_csv_files
from pipeline.load_s3 import upload_to_s3
from pipeline.load_snowflake import copy_into_raw
from pipeline.utils import get_logger

log = get_logger("pipeline.main")


def run() -> int:
    try:
        files = find_csv_files()
        if not files:
            log.error("no CSV files found - generate them with Synthea first")
            return 1
        upload_to_s3(files)
        copy_into_raw()
        log.info("pipeline finished successfully")
        return 0
    except Exception:
        log.exception("pipeline failed")
        return 1


if __name__ == "__main__":
    sys.exit(run())
