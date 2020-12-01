from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta

from airflow.operators.pipeline_plugin import HDXExtractOperator, Adm0Operator

from utils.dag_configuration import get_default_arguments, get_schedule_interval, get_catchup
from utils.config_parser import Config

from adm0_dags import create_adm0_dag

# Following are defaults which can be overridden later on
default_args = get_default_arguments()
schedule_interval = get_schedule_interval()
catchup = get_catchup()

config = Config()

country = "yemen"
geo_extent = "yem"

adm0_dag = create_adm0_dag(country=country, geo_extent=geo_extent, schedule_interval=schedule_interval, catchup=catchup, config=config, default_args=default_args)
