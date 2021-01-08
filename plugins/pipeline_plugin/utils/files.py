import os
import shutil
from pathlib import Path
import time

from pipeline_plugin.config import config
from pipeline_plugin.utils.google_cloud_storage import upload_file


CACHE_INVALID_AFTER_DAYS = 7


def copy_file(source_path, target_path):
    if config.use_remote_storage():
        upload_file(source_path, target_path)


def check_if_file_exists(filename):
    return os.path.exists(filename)


def get_file_age_in_days(filename):
    file_statistics = os.stat(filename)
    result_time_millisecond = time.time() - file_statistics.st_mtime
    return result_time_millisecond / 1000 / 60 / 60 / 24


def check_if_valid_cache(filename):
    if config.use_remote_storage():
        return False    
    if not check_if_file_exists(filename):
        return False
    return get_file_age_in_days(filename) < CACHE_INVALID_AFTER_DAYS


def get_base_path():
    return Path("/") / "opt" / "data"


def get_full_data_path(relative_path: Path):
    return get_base_path() / relative_path
