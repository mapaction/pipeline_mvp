from google.cloud import storage
from pipeline_plugin.config import config
from pathlib import Path


class GoogleCloudStorageClient:
    def __init__(self):
        if config.is_inside_gcp():
            self.storage_client = storage.Client()
        else:
            self.storage_client = storage.Client.from_service_account_json(Path(__file__).parent / "keyfile.json")

    def download_file_from_gcs(self, bucket_name: str, source_blob: str, destination_filename: str):
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob)
        blob.download_to_filename(destination_filename)

    def upload_file_to_gcs(self, bucket_name: str, destination_blob: str, source_filename: str):
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob)
        blob.upload_from_filename(source_filename)


if config.use_remote_storage():
    client = GoogleCloudStorageClient()


def upload_file(path: Path):
    bucket = config.get_data_bucket_name()
    blob = str(path)
    client.upload_file_to_gcs(bucket_name=bucket, destination_blob=blob, source_filename=str(path))


def download_file(path: Path):
    bucket = config.get_data_bucket_name()
    blob = str(path)
    client.download_file_from_gcs(bucket_name=bucket, source_blob=blob, destination_filename=str(path))
    return path
