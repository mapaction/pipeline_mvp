from airflow import DAG
from airflow_logic.dags.dags_utils.dag_configuration import (
    get_catchup,
    get_default_arguments,
    get_schedule_interval,
)
from airflow_logic.dags.dags_utils.hdx_dags_filler import fill_hdx_adm_dag
from config_access.config_parser import config

countries = config.get_countries()

# Defaults which can be overridden if needed
default_args = get_default_arguments()
schedule_interval = get_schedule_interval()
catchup = get_catchup()

with DAG(
    "hdx_adm",
    schedule_interval=schedule_interval,
    catchup=catchup,
    default_args=default_args,
) as dag:
    for country in countries:
        fill_hdx_adm_dag(dag, config, country)
