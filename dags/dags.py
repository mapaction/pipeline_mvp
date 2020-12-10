from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta

from airflow.operators.pipeline_plugin import HDXExtractOperator, HDXAdm0TransformOperator, HDXAdm1TransformOperator, \
    HDXRoadsTransformOperator, OSMExtractOperator

from utils.dag_configuration import get_default_arguments, get_schedule_interval, get_catchup
from utils.config_parser import Config

from hdx_adm_dags import create_hdx_adm_dag
from hdx_roads_dags import create_hdx_road_dag
from osm_roads_dags import create_osm_road_dag


# Following are defaults which can be overridden later on
default_args = get_default_arguments()
schedule_interval = get_schedule_interval()
catchup = get_catchup()

config = Config()

country = "yemen"

hdx_adm0_dag = create_hdx_adm_dag(country=country, schedule_interval=schedule_interval, catchup=catchup, config=config,
                                  default_args=default_args)
hdx_road_dag = create_hdx_road_dag(country=country, schedule_interval=schedule_interval, catchup=catchup, config=config,
                                   default_args=default_args)
osm_road_dag = create_osm_road_dag(country=country, schedule_interval=schedule_interval, catchup=catchup, config=config,
                                   default_args=default_args)
