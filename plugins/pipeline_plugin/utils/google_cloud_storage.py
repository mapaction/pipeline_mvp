from pathlib import Path

from airflow.contrib.hooks.gcs_hook import GoogleCloudStorageHook

from pipeline_plugin.config import config
from pipeline_plugin.utils.files import get_base_path

gcs_hook = GoogleCloudStorageHook()


def upload_file(path: Path):
    bucket = config.get_data_bucket_name()
    base_path = get_base_path()
    relative_path = path.relative_to(base_path)
    object = relative_path.to_posix()
    gcs_hook.upload(bucket=bucket, object=object, filename=path)


def download_file(path: Path):
    bucket = config.get_data_bucket_name()
    base_path = get_base_path()
    relative_path = path.relative_to(base_path)
    object = relative_path.to_posix()
    gcs_hook.download(bucket=bucket, object=object, filename=path)    
