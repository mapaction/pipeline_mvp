import os
import shutil
from pathlib import Path
import time
import functools

from pipeline_plugin.utils.google_cloud_storage import upload_file, download_file
from pipeline_plugin.utils.config import config


CACHE_INVALID_AFTER_DAYS = 7


def load_file(relative_source_path):
    if not os.path.exists(Path(relative_source_path).parent):
        os.makedirs(Path(relative_source_path).parent)

    if config.use_google_cloud_storage():
        filepath = download_file(relative_source_path)
    else:
        filepath = copy_file(config.get_remote_data_path(relative_source_path),
                             config.get_local_data_path(relative_source_path))
    return filepath


def save_file(relative_target_path):
    if config.use_google_cloud_storage():
        filepath = upload_file(relative_target_path)
    else:
        filepath = copy_file(config.get_local_data_path(relative_target_path),
                             config.get_remote_data_path(relative_target_path))
    return filepath


def copy_file(source_path, target_path):
    if not os.path.exists(Path(target_path).parent):
        os.makedirs(Path(target_path).parent)
    return shutil.move(source_path, target_path)


def create_download_folder(*args):
    for target_filepath in args:
        target_filepath = Path(target_filepath)
        if "." in  target_filepath.name:
            target_filepath = target_filepath.parent
        if not os.path.exists(target_filepath):
            os.makedirs(target_filepath)


def check_if_file_exists(filename):
    return os.path.exists(filename)


def get_file_age_in_days(filename):
    file_statistics = os.stat(filename)
    result_time_millisecond = time.time() - file_statistics.st_mtime
    return result_time_millisecond / 1000 / 60 / 60 / 24


def check_if_valid_cache(filename):
    environment = get_current_environment()
    if environment != "local":
        return False    
    if not check_if_file_exists(filename):
        return False
    return get_file_age_in_days(filename) < CACHE_INVALID_AFTER_DAYS


def get_base_path():
    return Path("/") / "opt" / "data"


def get_full_data_path(relative_path: Path):
    return get_base_path() / relative_path


def output_paths(*argument_names):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(**kwargs):
            f(**kwargs)
            for argument in argument_names:
                file_path = kwargs[argument]
                print(f"Saving output path {file_path}")
        return wrapper
    return decorator


def input_paths(*argument_names):
    def decorator(f):
        @functools.wraps(f)
        def wrapper(**kwargs):
            for argument in argument_names:
                file_path = kwargs[argument]
                print(f"Loading input path {file_path}")
            f(**kwargs)
        return wrapper
    return decorator


# def cache_outputs(*argument_names):
#     def wrap(f):
#         def wrapped_f(**kwargs):
#             all_cache_valid = True
#             for argument in argument_names:
#                 filename = kwargs[argument]
#                 if not check_if_valid_cache(filename):
#                     all_cache_valid = False
#                     break
#             if not all_cache_valid:
#                 print("At least one output file / directory not found or invalidated cache so calling the method")
#                 f(**kwargs)
#             else:
#                 print("All output files / directories have valid caches")
#         return wrapped_f
#     return wrap
