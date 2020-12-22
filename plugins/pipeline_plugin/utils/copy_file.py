import os
import shutil
from pathlib import Path


from pipeline_plugin.utils.environment import get_current_environment


def copy_file(source_path, target_path):
    environment = get_current_environment()
    if environment == "local":
        shutil.move(source_path, target_path)
    elif environment == "staging":
        print("Staging")
    elif environment == "production":
        print("Production")
