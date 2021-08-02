from airflow import DAG
from airflow_logic.dags.dags_utils.dag_configuration import (
    get_catchup,
    get_dags_configuration,
    get_default_arguments,
    get_schedule_interval,
)
from config_access.config_parser import config
from dags_utils.utils.hdx_dags_filler import (
    fill_hdx_adm_dag,
    fill_hdx_roads_dag,
)
from dags_utils.utils.osm_dags_filler import fill_osm_dag


# Defaults which can be overridden if needed
default_args = get_default_arguments()
schedule_interval = get_schedule_interval()
catchup = get_catchup()

countries = config.get_countries()
osm_datasets = get_dags_configuration()["osm"].keys()

for country in countries:
    with DAG(
        country + "_dag",
        schedule_interval=schedule_interval,
        catchup=catchup,
        default_args=default_args,
    ) as dag:
        for datatype in osm_datasets:
            fill_osm_dag(dag, config, datatype, country)
        globals()["osm_" + country + "dag_id"] = dag
        fill_hdx_adm_dag(dag, config, country)
        fill_hdx_roads_dag(dag, config, country)
