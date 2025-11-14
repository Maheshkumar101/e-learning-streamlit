import boto3
import os
from dotenv import load_dotenv
from botocore.client import Config

load_dotenv()

ACCESS_KEY = os.getenv("AWS_ACCESS_KEY_ID")
SECRET_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET_NAME = os.getenv("BACKBLAZE_BUCKET")
ENDPOINT = os.getenv("B2_S3_ENDPOINT")

# Create S3-compatible client for Backblaze


def get_b2_client():
    return boto3.client(
        "s3",
        endpoint_url=ENDPOINT,
        aws_access_key_id=ACCESS_KEY,
        aws_secret_access_key=SECRET_KEY,
        config=Config(signature_version="s3v4"),
        region_name="us-west-002"
    )


# Upload file object to Backblaze
def upload_fileobj(file_obj, filename):
    client = get_b2_client()
    client.upload_fileobj(
        file_obj,
        BUCKET_NAME,
        filename,
        ExtraArgs={"ACL": "public-read"}  # Make file public
    )
    return f"{ENDPOINT}/{BUCKET_NAME}/{filename}"
