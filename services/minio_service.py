import os
import uuid

from dotenv import load_dotenv
from minio import Minio
from minio.error import S3Error
from fastapi import HTTPException

load_dotenv()


MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY")
MINIO_BUCKET = os.getenv("MINIO_BUCKET")


if not all([
    MINIO_ENDPOINT,
    MINIO_ACCESS_KEY,
    MINIO_SECRET_KEY,
    MINIO_BUCKET
]):
    raise RuntimeError(
        "MinIO environment variables are not properly configured."
    )


minio_client = Minio(
    MINIO_ENDPOINT,
    access_key=MINIO_ACCESS_KEY,
    secret_key=MINIO_SECRET_KEY,
    secure=False
)


def upload_file_to_minio(
    file_data: bytes,
    file_name: str,
    content_type: str
) -> str:

    file_extension = os.path.splitext(file_name)[1]

    unique_file_name = (
        f"tickets/{uuid.uuid4()}{file_extension}"
    )

    try:
        from io import BytesIO

        minio_client.put_object(
            bucket_name=MINIO_BUCKET,
            object_name=unique_file_name,
            data=BytesIO(file_data),
            length=len(file_data),
            content_type=content_type
        )

    except S3Error:
        raise HTTPException(
            status_code=500,
            detail="Failed to upload image to MinIO"
        )

    file_url = (
        f"http://{MINIO_ENDPOINT}/{MINIO_BUCKET}/{unique_file_name}"
    )

    return file_url