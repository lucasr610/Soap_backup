"""Stub script for uploading files to Google Cloud Storage.

This implementation avoids network calls and simply returns the URI that would
be used for the upload. It can be expanded later if remote uploads become
allowed.
"""

from pathlib import Path
import argparse


def upload_to_gcs(file_path: str, bucket: str, object_name: str | None = None) -> str:
    """Return the simulated ``gs://`` URI for a file.

    Parameters
    ----------
    file_path: str
        Path to the file that would be uploaded.
    bucket: str
        Name of the target bucket.
    object_name: str | None
        Desired object name in the bucket. Defaults to the basename of
        ``file_path``.
    """
    return f"gs://{bucket}/{object_name or Path(file_path).name}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Simulate file upload to GCS")
    parser.add_argument("file", help="Path to file to upload")
    parser.add_argument("bucket", help="Target GCS bucket")
    parser.add_argument("--object", dest="object_name", help="Object name in bucket")
    args = parser.parse_args()
    uri = upload_to_gcs(args.file, args.bucket, args.object_name)
    print(f"Simulated upload to {uri}")


if __name__ == "__main__":
    main()
