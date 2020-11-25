import os
import shutil
from pathlib import Path


from pipeline_plugin.utils.environment import get_current_environment


def copy_file(source_path, target_path):
    environment = get_current_environment()
    if environment == "local":
        full_target_path = os.path.join("/opt/data", target_path)        
        shutil.move(source_path, full_target_path)
    elif environment == "staging":
        print("Staging")
