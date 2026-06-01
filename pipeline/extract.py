"""Locate the synthetic clinical CSVs produced by Synthea.

Generate them first (requires Java 17+):

    java -jar synthea-with-dependencies.jar --exporter.csv.export=true -p 1000

That writes patients.csv, conditions.csv, procedures.csv, medications.csv,
encounters.csv (and more) into ./output/csv/.
"""
from __future__ import annotations

import pathlib

from .config import SYNTHEA_CSV_DIR, TABLES
from .utils import get_logger

log = get_logger(__name__)


def find_csv_files(csv_dir: str = SYNTHEA_CSV_DIR) -> list[pathlib.Path]:
    """Return the expected Synthea CSV files that actually exist on disk."""
    base = pathlib.Path(csv_dir)
    found: list[pathlib.Path] = []
    for filename in TABLES:
        path = base / filename
        if path.exists():
            found.append(path)
        else:
            log.warning("expected file not found: %s", path)
    log.info("found %d of %d expected CSV files in %s", len(found), len(TABLES), csv_dir)
    return found
