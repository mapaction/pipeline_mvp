from pathlib import Path

from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook

from pipeline_plugin.utils.environment import get_current_environment
from pipeline_plugin.utils.files import get_base_path

gcs_hook = GoogleCloudStorageHook()


def get_bucket_name():
    environment = get_current_environment()
    if environment == "staging":
        return "mapaction-data-staging"
    elif environment == "production":
        return "mapaction-data-production"
    raise ValueError("Not in an environment with Google Cloud Storage buckets")


def upload_file(path: Path):
    bucket = get_bucket_name()
    base_path = get_base_path()
    relative_path = path.relative_to(base_path)
    object = relative_path.to_posix()
    gcs_hook.upload(bucket=bucket, object=object, filename=path)


def download_file(path: Path):
    bucket = get_bucket_name()
    base_path = get_base_path()
    relative_path = path.relative_to(base_path)
    object = relative_path.to_posix()
    gcs_hook.download(bucket=bucket, object=object, filename=path)    
