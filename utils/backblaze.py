# utils/backblaze.py
import os
import boto3
from botocore.client import Config

AWS_ENDPOINT = os.getenv("B2_S3_ENDPOINT")
AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
BUCKET = os.getenv("BACKBLAZE_BUCKET")

_session = None

def get_s3():
    global _session
    if _session is None:
        _session = boto3.session.Session()
    s3 = _session.client(
        "s3",
        endpoint_url=AWS_ENDPOINT,
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        config=Config(signature_version="s3v4"),
    )
    return s3

def upload_fileobj(file_obj, key: str) -> str:
    s3 = get_s3()
    # file_obj may be a Streamlit UploadedFile; use .getbuffer() or .read()
    try:
        s3.upload_fileobj(file_obj, BUCKET, key)
    except Exception:
        # Try reading bytes and using put_object
        file_obj.seek(0)
        s3.put_object(Bucket=BUCKET, Key=key, Body=file_obj.read())
    return f"{AWS_ENDPOINT}/{BUCKET}/{key}"

def list_objects(prefix=""):
    s3 = get_s3()
    resp = s3.list_objects_v2(Bucket=BUCKET, Prefix=prefix)
    return resp.get("Contents", [])
