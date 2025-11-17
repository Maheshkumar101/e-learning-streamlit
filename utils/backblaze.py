# utils/backblaze.py
import os
import boto3
from dotenv import load_dotenv
from botocore.client import Config
from pathlib import Path

load_dotenv()

B2_KEY_ID = os.getenv("B2_KEY_ID")
B2_APP_KEY = os.getenv("B2_APP_KEY")
B2_BUCKET = os.getenv("B2_BUCKET")
# example: https://s3.us-east-005.backblazeb2.com
B2_ENDPOINT = os.getenv("B2_ENDPOINT")

# If upload fails, optionally save locally to 'assets/uploads'
FALLBACK_LOCAL = True
LOCAL_UPLOAD_DIR = Path("assets/uploads")
LOCAL_UPLOAD_DIR.mkdir(parents=True, exist_ok=True)


def _get_client():
    if not all([B2_KEY_ID, B2_APP_KEY, B2_BUCKET, B2_ENDPOINT]):
        raise RuntimeError(
            "Backblaze env vars missing. Set B2_KEY_ID, B2_APP_KEY, B2_BUCKET, B2_ENDPOINT in .env")
    # Use stable config for compat
    return boto3.client(
        "s3",
        endpoint_url=B2_ENDPOINT,
        aws_access_key_id=B2_KEY_ID,
        aws_secret_access_key=B2_APP_KEY,
        config=Config(signature_version="s3v4"),
        region_name="us-east-1"  # region_name doesn't affect B2 but boto3 wants a value
    )


def upload_fileobj(file_obj, filename):
    """
    Upload a file-like object (streamlit uploaded file) to Backblaze B2 via S3 API.
    - file_obj: file-like object with .read() (Streamlit's UploadedFile is acceptable)
    - filename: e.g. "thumbnails/img.png" or "pdfs/course123.pdf"
    Returns: public URL string on success, or None on failure (and may fallback to local path).
    """
    try:
        client = _get_client()
        # Reset file pointer to start (UploadedFile may already be at start)
        try:
            file_obj.seek(0)
        except Exception:
            pass

        client.upload_fileobj(
            Fileobj=file_obj,
            Bucket=B2_BUCKET,
            Key=filename,
            ExtraArgs={"ACL": "public-read",
                       "ContentType": getattr(file_obj, "type", "binary/octet-stream")}
        )

        return f"{B2_ENDPOINT.rstrip('/')}/{B2_BUCKET}/{filename}"
    except Exception as e:
        # Don't leak secrets in logs; print a compact message
        print("B2 upload failed:", str(e))
        if FALLBACK_LOCAL:
            try:
                target = LOCAL_UPLOAD_DIR / Path(filename).name
                # Reset pointer and write locally
                try:
                    file_obj.seek(0)
                except Exception:
                    pass
                with open(target, "wb") as f:
                    f.write(file_obj.read())
                # Return local relative path so UI can show it
                return str(target.as_posix())
            except Exception as e2:
                print("Local fallback save failed:", e2)
        return None
