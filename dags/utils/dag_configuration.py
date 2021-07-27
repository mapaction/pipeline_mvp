from datetime import datetime, timedelta
import os


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


def get_catchup():
    return not os.getenv("ENVIRONMENT") in ("DEVELOP", "LOCAL")


def get_schedule_interval():
    return None if os.getenv("ENVIRONMENT") in ("DEVELOP", "LOCAL") else "@daily"
