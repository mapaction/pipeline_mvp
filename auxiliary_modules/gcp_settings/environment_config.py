import os
from pathlib import Path

from airflow.models import Variable
import yaml


class Config:
    def __init__(self, path=None):
        if path is None:
            if os.environ.get("ENVIRONMENT") == "LOCAL":
                path = Path(os.getcwd()) / "gcp_settings"
            else:
                if self.is_inside_kubernetes_pod():
                    path = Path("/") / "usr" / "src" / "gcp_settings"
                else:
                    path = Path("/") / "home" / "airflow" / "gcs" / "gcp_settings"

        with open(path / "config.yaml") as f:
            self.raw_config = yaml.safe_load(f)

        with open(path / f"config.{os.environ.get('ENVIRONMENT').lower()}.yaml") as f:
            self.environment_config = yaml.safe_load(f)
            self.raw_config.update(self.environment_config)

    @staticmethod
    def is_inside_gcp():
        return os.environ.get("GCP") == "TRUE"

    @staticmethod
    def is_inside_kubernetes_pod():
        return os.getenv("INSIDE_KUBERNETES_POD") == "TRUE"

    @staticmethod
    def use_kubernetes():
        return os.environ.get("ENVIRONMENT") != "LOCAL"

    @staticmethod
    def use_remote_storage():
        return os.environ.get("ENVIRONMENT") != "LOCAL"

    @staticmethod
    def get_remote_data_path(relative_path):
        return os.path.join(Path("airflow/data"), relative_path)

    @staticmethod
    def get_local_data_path(relative_path):
        if os.environ.get("ENVIRONMENT") == "LOCAL":
            return Path("/") / "opt" / "airflow" / "data" / relative_path           #TODO This is basically hardcoded and should be passed in
        else:
            return Path("/") / "usr" / "src" / "data" / relative_path

    @staticmethod
    def get_docker_image_version():
        return Variable.get("DOCKER_IMAGE_VERSION", default_var="latest")

    def get_data_bucket_name(self):
        return self.raw_config["googleCloudStorage"]["dataBucketName"]

    def get_docker_image(self):
        return (
            self.raw_config["docker"]["imageName"]
            + ":"
            + self.get_docker_image_version()
        )


config = Config()
