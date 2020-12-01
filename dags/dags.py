from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta

from airflow.operators.pipeline_plugin import HDXExtractOperator, Adm0Operator

from utils.default_args import get_default_arguments
from utils.config_parser import Config

from adm0_dags import create_adm0_dag

# Following are defaults which can be overridden later on
default_args = get_default_arguments()
config = Config()

country = "yemen"
geo_extent = "yem"

adm0_dag = create_adm0_dag(country=country, geo_extent=geo_extent, config=config, default_args=default_args)
