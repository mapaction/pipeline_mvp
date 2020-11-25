import os

from processing.utils.environment import get_current_environment


def write_data(data, filename):
    environment = get_current_environment()
    if environment == "local":
        with open(os.path.join("data", filename), 'w') as f:
            f.write("Hoi")
    elif environment == "staging":
        print("Staging")
