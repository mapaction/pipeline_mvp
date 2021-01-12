import os
import yaml
from pathlib import Path


class Config:
    def __init__(self, path=None):
        if path is None:
            if os.environ.get("ENVIRONMENT") == "LOCAL":
                path = Path(os.getcwd()) / "plugins" / "pipeline_plugin" / "config"
            else:
                path = Path("/") / "usr" / "src" / "pipeline_plugin" / "config"
        with open(path / "config.yaml") as f:
            self.raw_config = yaml.safe_load(f)
        with open(path / f"config.{os.environ.get(" ENVIRONMENT ").lower()}.yaml") as f:
            self.environment_config = yaml.safe_load(f)
            self.raw_config.update(self.environment_config)

    def use_kubernetes(self):
        return os.environ.get("ENVIRONMENT") != "LOCAL"

    def use_remote_storage(self):
        return os.environ.get("ENVIRONMENT") != "LOCAL"

    def get_local_data_path(self, relative_path):
        if os.environ.get("ENVIRONMENT") == "LOCAL":
            return Path("/") / "opt" / "data" / relative_path
        else:
            return Path("/") / "usr" / "src" / "data" / relative_path

    def get_data_bucket_name(self):
        return self.raw_config["googleCloudStorage"]["dataBucketName"]


config = Config()
