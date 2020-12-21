import os
import shutil
from pathlib import Path


from pipeline_plugin.utils.environment import get_current_environment
from pipeline_plugin.utils.CloudStorageClient import GoogleCloudStorageClient

def copy_file(source_path, target_path):
    environment = get_current_environment()
    if environment == "local":
        shutil.move(source_path, target_path)
    elif environment == "DEVELOP":
        client = GoogleCloudStorageClient()
        client.upload_file_to_gcs(
            bucket_name="europe-west2-mapaction-deve-8c266b1d-bucket",
            gcs_filename=f"data/output_folder/{Path(target_path).name}",
            input_filename=source_path
        )
    elif environment == "production":
        print("Production")
