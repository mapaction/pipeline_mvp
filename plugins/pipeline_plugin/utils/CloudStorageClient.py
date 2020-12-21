from google.cloud import storage
from google.auth.exceptions import DefaultCredentialsError


class GoogleCloudStorageClient:
    def __init__(self):
        try:
            self.storage_client = storage.Client()
        except DefaultCredentialsError:
            self.storage_client = storage.Client.from_service_account_json("LOCAL CREDENTIALS")

    def get_file_from_gcs(self, bucket_name: str, gcs_filename: str, output_filename: str):
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(gcs_filename)
        blob.download_to_filename(output_filename)

    def upload_file_to_gcs(self, bucket_name: str, gcs_filename: str, input_filename: str):
        bucket = self.storage_client.bucket(bucket_name)
        blob = bucket.blob(gcs_filename)
        blob.upload_from_filename(input_filename)
