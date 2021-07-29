from airflow import DAG

from dags_utils.utils.config_parser import config

from dags.dags_utils.dag_configuration import (
    get_catchup,
    get_dags_configuration,
    get_default_arguments,
    get_schedule_interval,
)
from dags_utils.utils.osm_dags_filler import fill_osm_dag

# Defaults which can be overridden if needed
default_args = get_default_arguments()
schedule_interval = get_schedule_interval()
catchup = get_catchup()

countries = config.get_countries()
osm_datasets = get_dags_configuration()["osm"].keys()

for datatype in osm_datasets:
    with DAG(
        "osm_" + datatype,
        schedule_interval=schedule_interval,
        catchup=catchup,
        default_args=default_args,
    ) as dag:
        for country in countries:
            fill_osm_dag(dag, config, datatype, country)
        globals()["osm_" + datatype + "dag_id"] = dag
