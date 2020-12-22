import os
import shutil
from pathlib import Path
import time

from pipeline_plugin.utils.environment import get_current_environment


CACHE_INVALID_AFTER_DAYS = 7


def copy_file(source_path, target_path):
    environment = get_current_environment()
    if environment == "local":
        shutil.move(source_path, target_path)
    elif environment == "staging":
        print("Staging")
    elif environment == "production":
        print("Production")


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
    def wrap(f):
        def wrapped_f(**kwargs):
            f(**kwargs)
            for argument in argument_names:
                file_path = kwargs[argument]
                print(f"Saving output path {file_path}")
        return wrapped_f
    return wrap


def input_paths(*argument_names):
    def wrap(f):
        def wrapped_f(**kwargs):
            for argument in argument_names:
                file_path = kwargs[argument]
                print(f"Loading input path {file_path}")
            f(**kwargs)
        return wrapped_f
    return wrap


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
