import os
from pathlib import Path


class Config:
    def get_current_environment(self):
        return os.getenv("ENVIRONMENT")

    def get_local_data_path(self, relative_path):
        return os.path.join(os.getenv("LOCAL_DATA_FOLDER"), relative_path)

    def get_remote_data_path(self, relative_path):
        return os.path.join(Path("data"), relative_path)

    def use_google_cloud_storage(self) -> bool:
        gcs = True
        if os.getenv("ENVIRONMENT") == "LOCAL":
            gcs = False
        return gcs

    def get_gcs_bucket_name(self):
        return "europe-west2-mapaction-deve-542e8027-bucket"

    def get_gcs_base_path(self):
        return "data"


config = Config()
