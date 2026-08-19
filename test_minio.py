from services.minio_service import minio_client, MINIO_BUCKET


try:
    if minio_client.bucket_exists(MINIO_BUCKET):
        print("SUCCESS: MinIO connected successfully!")
        print(f"Bucket found: {MINIO_BUCKET}")
    else:
        print("ERROR: MinIO connected, but bucket was not found.")

except Exception as e:
    print("ERROR: Could not connect to MinIO.")
    print(e)