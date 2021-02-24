import logging
import os
import tempfile
from airflow.utils.decorators import apply_defaults
from pipeline_plugin.config import config
from pipeline_plugin.utils.google_cloud_storage import GoogleCloudStorageClient
from pipeline_plugin.utils.files import get_base_path as data_dir

from pipeline_plugin.operators.BaseMapActionOperator import MapActionOperator
import subprocess

logger = logging.getLogger(__name__)


def sync_from_gcp_to_gdrive(gcp_path: str, gdrive_folder_id: str):
    
    # On GCP `airflow_home` exists and returns a read/writable location
    # On localhost None will result in a tempdir in /tmp which is a read/writable location 
    home_dir = os.environ.get('airflow_home', None)
    
    # if not home_dir:
    #    raise RuntimeError('Expected to find value for environment varible `airflow_home`')
    
    # _, service_auth_path = tempfile.mkstemp(dir=data_dir(), suffix='.json')

    try:
        service_auth_temp_dir = tempfile.TemporaryDirectory(dir=home_dir)
        service_auth_path = os.path.join(service_auth_temp_dir.name, 'gdrive_auth.json')
        logger.info(f'creating temporary service auth file = {service_auth_path}')
        os.mknod(service_auth_path)    
        logger.info(f'temporary service auth file exists (expect true) = {os.path.exists(service_auth_path)}')
        logger.info(f'temporary service auth file size (expect zero) = {os.path.getsize(service_auth_path)}')

        if config.is_inside_gcp():
            logger.info(f'Attempting to update temporary service auth file from GoogleCloudStorageClient')
            gcsc = GoogleCloudStorageClient()
            gcsc.download_file_from_gcs(
                bucket_name=config.get_rclone_service_account_auth_bucket(),
                source_blob=config.get_rclone_service_account_auth_file(),
                destination_filename=service_auth_path
            )

            logger.info(f'temporary service auth file exists (expect true) = {os.path.exists(service_auth_path)}')
            logger.info(f'temporary service auth file size (expect non-zero) = {os.path.getsize(service_auth_path)}')

            test_cmd = [f'ls',
                f'-la',
                f'{service_auth_path}'
            ]
            logger.info(f'test_cmd =```{(" " .join(test_cmd))}```')
            test_cmd_output = subprocess.check_output(test_cmd)
            logger.info(f'test_cmd_output = {test_cmd_output}')

            rclone_gcp_ls_cmd = [f'rclone',
                f'ls',
                f':"google cloud storage":{gcp_path}/data',
                f'--gcs-service-account-file={service_auth_path}'
            ]

            rclone_gdrive_ls_cmd = [f'rclone',
                f'ls',
                f':drive:data',
                f'--drive-scope=drive',
                f'--drive-service-account-file={service_auth_path}',
                f'--drive-team-drive={gdrive_folder_id}',
                f'--drive-auth-owner-only'
            ]

            rclone_sync_cmd = [f'rclone',
                f'sync',
                f':"google cloud storage":{gcp_path}/data',
                f'--gcs-service-account-file={service_auth_path}',
                f':drive:data',
                f'--drive-scope=drive',
                f'--drive-service-account-file={service_auth_path}',
                f'--drive-team-drive={gdrive_folder_id}',
                f'--drive-auth-owner-only']

            for rclone_cmd in [rclone_gcp_ls_cmd, rclone_gdrive_ls_cmd, rclone_sync_cmd]:
                try:
                    logger.info(f'rclone_cmd =```{(" ".join(rclone_cmd))}```')
                    rclone_output = subprocess.check_output(rclone_cmd)
                    logger.info(f'rclone_output = {rclone_output}')
                except subprocess.CalledProcessError as cpe:
                    logger.error(f'error whilst processing rclone_cmd= {rclone_cmd}')
                    logger.error(f'   cmd as called = {cpe.cmd}')
                    logger.error(f'   return code = {cpe.returncode}')
                    logger.error(f'   output = {cpe.output}')
        else:
            logger.info(f'Attempting to update temporary service auth file from GoogleCloudStorageClient')

            test_cmd = [f'ls',
                f'-la',
                f'{service_auth_path}'
            ]


            logger.info(f'temporary service auth file exists (expect true) = {os.path.exists(service_auth_path)}')
            logger.info(f'temporary service auth file size (expect non-zero) = {os.path.getsize(service_auth_path)}')

            test_cmd = [f'ls',
                f'-la',
                f'{service_auth_path}'
            ]
            logger.info(f'test_cmd =```{(" ".join(test_cmd))}```')
            test_cmd_output = subprocess.check_output(test_cmd)
            logger.info(f'test_cmd_output = {test_cmd_output}')
            logger.info(f'compeleted with real file')

            # test_cmd = [f'ls',
            #     f'-la',
            #     f'{service_auth_path}doesnotexist'
            # ]
            # logger.info(f'test_cmd =```{(" ".join(test_cmd))}```')
            # test_cmd_output = subprocess.check_output(test_cmd)
            # logger.info(f'test_cmd_output = {test_cmd_output}')
            # logger.info(f'compeleted with non existant file')
    finally:
        service_auth_temp_dir.cleanup()
        # os.remove(service_auth_path)


class RCloneOperator(MapActionOperator):
    @apply_defaults
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(method=sync_from_gcp_to_gdrive, 
                         arguments={
                             "gcp_path": config.get_data_bucket_name(),
                             "gdrive_folder_id": config.get_google_drive_output_folder_id()
                         },
                         *args, **kwargs)
