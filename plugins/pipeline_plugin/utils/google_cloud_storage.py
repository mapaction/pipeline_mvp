# from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook
from google.cloud import storage
from google.auth.exceptions import DefaultCredentialsError

from pipeline_plugin.utils.config import config

# gcs_hook = GoogleCloudStorageHook()
from pathlib import Path

class GoogleCloudStorageClient:
    def __init__(self):
        try:
            self.storage_client = storage.Client()
        except DefaultCredentialsError:
            from pathlib import Path
            self.storage_client = storage.Client.from_service_account_json(Path(__file__).parent / "keyfile.json")

    def download_file_from_gcs(self, bucket_name: str, source_blob: str, destination_filename: str):
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(source_blob)
        blob.download_to_filename(destination_filename)

    def upload_file_to_gcs(self, bucket_name: str, destination_blob: str, source_filename: str):
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob)
        blob.upload_from_filename(source_filename)


client = GoogleCloudStorageClient()

def upload_file(path: Path):
    bucket = config.get_gcs_bucket_name()
    blob = str(path)
    client.upload_file_to_gcs(bucket_name=bucket, destination_blob=blob, source_filename=str(path))
    # gcs_hook.upload(bucket=bucket, object=object, filename=path)


def download_file(path: Path):
    bucket = config.get_gcs_bucket_name()
    blob = str(path)
    client.download_file_from_gcs(bucket_name=bucket, source_blob=blob, destination_filename=str(path))
    return path
    # gcs_hook.download(bucket=bucket, object=object, filename=path)


# def upload_file(path: Path):
#     bucket = config.get_gcs_bucket_name()
#     base_path = config.get_gcs_base_path()
#     relative_path = path.relative_to(base_path)
#     object = relative_path.to_posix()
#     gcs_hook.upload(bucket=bucket, object=object, filename=path)
#
#
# def download_file(path: Path):
#     bucket = config.get_gcs_bucket_name()
#     base_path = config.get_gcs_base_path()
#     relative_path = path.relative_to(base_path)
#     object = relative_path.to_posix()
#     gcs_hook.download(bucket=bucket, object=object, filename=path)
