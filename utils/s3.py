import os
import uuid

import boto3
from botocore.exceptions import BotoCoreError, ClientError
from fastapi import HTTPException


AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_S3_BUCKET = os.getenv("AWS_S3_BUCKET")


if not all([
    AWS_ACCESS_KEY_ID,
    AWS_SECRET_ACCESS_KEY,
    AWS_REGION,
    AWS_S3_BUCKET
]):
    raise RuntimeError(
        "AWS S3 environment variables are not properly configured."
    )


s3_client = boto3.client(
    "s3",
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)


def upload_file_to_s3(
    file_data: bytes,
    file_name: str,
    content_type: str
) -> str:

    file_extension = os.path.splitext(file_name)[1]

    unique_file_name = (
        f"tickets/{uuid.uuid4()}{file_extension}"
    )

    try:
        s3_client.put_object(
            Bucket=AWS_S3_BUCKET,
            Key=unique_file_name,
            Body=file_data,
            ContentType=content_type
        )

    except (BotoCoreError, ClientError):
        raise HTTPException(
            status_code=500,
            detail="Failed to upload image to AWS S3"
        )

    file_url = (
        f"https://{AWS_S3_BUCKET}.s3."
        f"{AWS_REGION}.amazonaws.com/"
        f"{unique_file_name}"
    )

    return file_url