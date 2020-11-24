import os
from datetime import datetime, timedelta


def local_arguments():
    return {
        'schedule_interval': None
    }


def get_default_arguments():
    default_arguments = {
        'owner': 'MapAction',
        'depends_on_past': False,
        'start_date': datetime(2020, 11, 25),
        'email': ['dennis.dickmann@digital-power.com'],
        'email_on_failure': False,
        'email_on_retry': False,
        'retries': 1,
        'retry_delay': timedelta(minutes=1),
    }
    if os.getenv("ENVIRONMENT") == "local":
        additional_arguments = local_arguments()
    default_arguments.update(additional_arguments)
    return default_arguments
