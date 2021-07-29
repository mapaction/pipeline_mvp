from datetime import datetime, timedelta
import os

from pipeline_plugin.transform.default_transform import default_transform


# TODO: create DagsConfig class, store args and config in .yaml
def get_default_arguments():
    default_arguments = {
        "owner": "MapAction",
        "depends_on_past": False,
        "start_date": datetime(2020, 1, 1),
        "email": ["dennis.dickmann@digital-power.com"],
        "email_on_failure": False,
        "email_on_retry": False,
        "retries": 1,
        "retry_delay": timedelta(minutes=1),
    }
    return default_arguments


def get_dags_configuration():
    dags_config = {
        "osm": {
            "roads": {"transform": default_transform},
            "airports": {"transform": default_transform},
            "rail": {"transform": default_transform},
            "lakes": {"transform": default_transform},
            "places": {"transform": default_transform},
            "rivers": {"transform": default_transform},
            "seaports": {"transform": default_transform},
            "seas": {"transform": default_transform},
        }
    }
    return dags_config


def get_catchup():
    return not os.getenv("ENVIRONMENT") in ("DEVELOP", "LOCAL")


def get_schedule_interval():
    return None if os.getenv("ENVIRONMENT") in ("DEVELOP", "LOCAL") else "@daily"
