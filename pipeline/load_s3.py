"""Upload the raw Synthea CSVs to the S3 Bronze layer."""
from __future__ import annotations

import pathlib

import boto3
from tenacity import retry, stop_after_attempt, wait_exponential

from .config import S3Config
from .utils import get_logger

log = get_logger(__name__)


@retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, max=10))
def _upload_one(s3client, path: pathlib.Path, bucket: str, key: str) -> None:
    s3client.upload_file(str(path), bucket, key)


def upload_to_s3(files: list[pathlib.Path], cfg: S3Config | None = None) -> int:
    """Upload each file to s3://<bucket>/<prefix>/<filename>. Returns count."""
    cfg = cfg or S3Config()
    if not cfg.bucket:
        raise ValueError("S3_BUCKET is not set")
    s3client = boto3.client("s3")
    count = 0
    for path in files:
        key = f"{cfg.prefix}/{path.name}"
        log.info("uploading %s -> s3://%s/%s", path.name, cfg.bucket, key)
        _upload_one(s3client, path, cfg.bucket, key)
        count += 1
    log.info("uploaded %d files to s3://%s/%s", count, cfg.bucket, cfg.prefix)
    return count
