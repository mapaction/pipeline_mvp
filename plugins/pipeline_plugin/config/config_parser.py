import os
import yaml
from pathlib import Path


class Config:
    def __init__(self, path=None):
        if path is None:
            if os.environ.get("ENVIRONMENT") == "LOCAL":
                path = Path(os.getcwd()) / "plugins" / "pipeline_plugin" / "config"
            else:
                if self.is_inside_kubernetes_pod():
                    path = Path("/") / "usr" / "src" / "pipeline_plugin" / "config"
                else:
                    path = Path("/") / "home" / "airflow" / "gcs" / "plugins" / "pipeline_plugin" / "config"

        with open(path / "config.yaml") as f:
            self.raw_config = yaml.safe_load(f)

        with open(path / f"config.{os.environ.get('ENVIRONMENT').lower()}.yaml") as f:
            self.environment_config = yaml.safe_load(f)
            self.raw_config.update(self.environment_config)

    def is_inside_gcp(self):
        return os.environ.get("GCP") == "TRUE"

    def is_inside_kubernetes_pod(self):
        return os.getenv("INSIDE_KUBERNETES_POD") == "TRUE"

    def use_kubernetes(self):
        return os.environ.get("ENVIRONMENT") != "LOCAL"

    def use_remote_storage(self):
        return os.environ.get("ENVIRONMENT") != "LOCAL"

    def get_remote_data_path(self, relative_path):
        return os.path.join(Path("data"), relative_path)

    def get_local_data_path(self, relative_path):
        if os.environ.get("ENVIRONMENT") == "LOCAL":
            return Path("/") / "opt" / "data" / relative_path
        else:
            return Path("/") / "usr" / "src" / "data" / relative_path

    def get_data_bucket_name(self):
        return self.raw_config["googleCloudStorage"]["dataBucketName"]

    def get_docker_image(self):
        return self.raw_config["docker"]["imageName"] + ":" + self.raw_config["docker"]["imageVersion"]

    def get_google_drive_output_folder_id(self):
        return self.raw_config["RCloneSync"]["gdrive_folder_id"]

    def get_rclone_service_account_auth_bucket(self):
        return self.raw_config["RCloneSync"]["service_account_auth_bucket"]

    def get_rclone_service_account_auth_file(self):
        return self.raw_config["RCloneSync"]["service_account_auth_file"]

config = Config()
