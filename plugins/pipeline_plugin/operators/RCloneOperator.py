import logging
import os
import tempfile
from airflow.utils.decorators import apply_defaults
from pipeline_plugin.config import config
from pipeline_plugin.utils.google_cloud_storage import GoogleCloudStorageClient

from pipeline_plugin.operators.BaseMapActionOperator import MapActionOperator
import subprocess

logger = logging.getLogger(__name__)


def sync_from_gcp_to_gdrive(gcp_path: str, gdrive_folder_id: str):

    _, service_account_auth_path = tempfile.mkstemp(dir='/usr/local/airflow/plugins', suffix='.json')
    logger.info(f'creating temporary service auth file = {service_account_auth_path}')
    logger.info(f'temporary service auth file exists (expect true) = {os.path.exists(service_account_auth_path)}')
    logger.info(f'temporary service auth file size (expect zero) = {os.path.getsize(service_account_auth_path)}')

    try:
        if config.is_inside_gcp():
            logger.info(f'Attempting to update temporary service auth file from GoogleCloudStorageClient')
            gcsc = GoogleCloudStorageClient()
            gcsc.download_file_from_gcs(
                bucket_name=config.get_rclone_service_account_auth_bucket(),
                source_blob=config.get_rclone_service_account_auth_file(),
                destination_filename=service_account_auth_path
            )

            logger.info(f'temporary service auth file exists (expect true) = {os.path.exists(service_account_auth_path)}')
            logger.info(f'temporary service auth file size (expect non-zero) = {os.path.getsize(service_account_auth_path)}')

            rclone_cmd = [f'rclone',
                f'sync',
                f':"google cloud storage":{gcp_path}',
                f'--gcs-service-account-file={service_account_auth_path}',
                f':drive:',
                f'--drive-scope=drive',
                f'--drive-service-account-file={service_account_auth_path}"',
                f'--drive-team-drive={gdrive_folder_id}',
                f'--drive-auth-owner-only']

            subprocess.check_call(rclone_cmd)
        else:
            logger.info(f'Attempting to update temporary service auth file from GoogleCloudStorageClient')

            test_cmd = [f'ls',
                f'-la',
                f'{service_account_auth_path}'
            ]

            logger.info(f'temporary service auth file exists (expect true) = {os.path.exists(service_account_auth_path)}')
            logger.info(f'temporary service auth file size (expect non-zero) = {os.path.getsize(service_account_auth_path)}')

            subprocess.check_call(test_cmd)          
            logger.info(f'compeleted with real file')

            test_cmd = [f'ls',
                f'-la',
                f'{service_account_auth_path}doesnotexist'
            ]
            subprocess.check_call(test_cmd)          
            logger.info(f'compeleted with non existant file')

    finally:
        os.remove(service_account_auth_path)


class RCloneOperator(MapActionOperator):
    @apply_defaults
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(method=sync_from_gcp_to_gdrive, 
                         arguments={
                             "gcp_path": config.get_data_bucket_name(),
                             "gdrive_folder_id": config.get_google_drive_output_folder_id()
                         },
                         *args, **kwargs)
