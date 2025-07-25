from pathlib import Path
import argparse

from google.cloud import storage


def upload_to_gcs(file_path: str, bucket: str, object_name: str | None = None) -> str:
    client = storage.Client()
    bucket_obj = client.bucket(bucket)
    blob = bucket_obj.blob(object_name or Path(file_path).name)
    blob.upload_from_filename(file_path)
    return f"gs://{bucket}/{blob.name}"


def main() -> None:
    parser = argparse.ArgumentParser(description="Upload file to Google Cloud Storage")
    parser.add_argument("file", help="Path to file to upload")
    parser.add_argument("bucket", help="Target GCS bucket")
    parser.add_argument("--object", help="Object name in bucket")
    args = parser.parse_args()
    uri = upload_to_gcs(args.file, args.bucket, args.object)
    print(f"Uploaded to {uri}")


if __name__ == "__main__":
    main()
