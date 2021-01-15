from google.cloud import storage
from pipeline_plugin.config import config
from pathlib import Path
import os


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

    def download_folder_from_gcs(self, bucket_name: str, source_folder: str, destination_folder: str):
        bucket = self.storage_client.bucket(bucket_name)
        blobs = bucket.list_blobs(prefix=source_folder)
        for blob in blobs:
            filename = blob.name.split('/')[-1]
            blob.download_to_filename(Path(destination_folder) / filename)

    def upload_file_to_gcs(self, bucket_name: str, destination_blob: str, source_filename: str):
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob)
        blob.upload_from_filename(source_filename)

    def upload_folder_to_gcs(self, bucket_name, destination_folder: str, source_folder: str):
        bucket = self.storage_client.bucket(bucket_name)
        for subdir, dirs, filenames in os.walk(source_folder):
            for filename in filenames:
                blob = bucket.blob(destination_folder + "/" + subdir + "/" + filename)
                blob.upload_from_filename(Path(source_folder) / subdir / filename)

    def file_exists_gcs(self, bucket_name: str, destination_blob: str):
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob)
        return blob.exists()

if config.use_remote_storage():
    client = GoogleCloudStorageClient()


def upload_path(path: Path):
    bucket = config.get_data_bucket_name()
    if os.path.isdir(path):
        client.upload_folder_to_gcs(bucket_name=bucket, destination_folder=path, source_folder=path)
    else:
        blob = str(path)
        client.upload_file_to_gcs(bucket_name=bucket, destination_blob=blob, source_filename=str(path))


def download_path(path: Path):
    bucket = config.get_data_bucket_name()
    if client.file_exists_gcs(bucket):
        blob = str(path)
        client.download_file_from_gcs(bucket_name=bucket, source_blob=blob, destination_filename=str(path))
    else:
        client.download_folder_from_gcs(bucket_name=bucket, source_folder=path, destination_folder=path)
    return path
