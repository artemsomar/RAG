import boto3
import uuid
from pathlib import Path
from botocore.client import Config
from fastapi import UploadFile
from src.config import settings

print(f"DEBUG: Connecting to S3 with User: '{settings.s3.access_key}'")

s3_client = boto3.client(
    "s3",
    endpoint_url=settings.s3.endpoint_url,
    aws_access_key_id=settings.s3.access_key,
    aws_secret_access_key=settings.s3.access_secret_key,
    region_name=settings.s3.region,
    config=Config(signature_version="s3v4", s3={"addressing_style": "path"}),
)


BUCKET_NAME = settings.s3.bucket_name


def upload_file(file: UploadFile) -> dict:
    ext = Path(file.filename).suffix
    key = f"{uuid.uuid4()}{ext}"

    file.file.seek(0)

    s3_client.upload_fileobj(
        file.file, BUCKET_NAME, key, ExtraArgs={"ContentType": file.content_type}
    )

    base_url = settings.s3.endpoint_url
    if "minio" in base_url:
        base_url = base_url.replace("minio", "localhost")

    return {
        "key": key,
        "url": f"{base_url}/{BUCKET_NAME}/{key}",
        "media_type": file.content_type,
        "name": file.filename,
    }


def delete_file(key: str) -> None:
    s3_client.delete_object(Bucket=BUCKET_NAME, Key=key)
