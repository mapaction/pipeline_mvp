import os

from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta

from config import config

from airflow.operators.pipeline_plugin import OSMExtractOperator, OSMRoadsTransformOperator


def create_osm_road_dag(countries, schedule_interval, catchup, default_args):
    dag = DAG(f"osm_roads", schedule_interval=schedule_interval, catchup=catchup, default_args=default_args)

    for country in countries:
        osm_roads_extract = OSMExtractOperator(
            task_id=f"{country}_osm_roads_extract",
            osm_url=config.get_osm_url(country=country),
            country_iso2=config.get_iso2(country=country),
            schema_filename=config.get_osm_roads_tags_schema(country=country),
            osm_output_filename=config.get_osm_roads_raw_osm(country=country),
            gpkg_output_filename=config.get_osm_roads_raw_gpkg(country=country),
            dag=dag
        )

        source="osm"
        roads_transform = OSMRoadsTransformOperator(
            task_id=f"{country}_osm_roads_transform",
            source=source,
            input_filename=config.get_osm_roads_raw_gpkg(country=country),
            output_filename=config.get_osm_roads_processed_filename(country=country),
            crs=config.get_crs(),
            schema_mapping=config.get_roads_schema_mapping(source=source),
            dag=dag
        )

        osm_roads_extract >> roads_transform
    return dag
