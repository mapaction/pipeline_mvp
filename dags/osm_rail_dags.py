from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta

from country_config import config

from airflow.operators.pipeline_plugin import OSMExtractOperator, OSMRailTransformOperator


def create_osm_rail_dag(countries, schedule_interval, catchup, default_args):
    dag = DAG(f"osm_rail", schedule_interval=schedule_interval, catchup=catchup, default_args=default_args)
    for country in countries:
        osm_rail_extract = OSMExtractOperator(
            task_id=f"{country}_osm_rail_extract",
            osm_url=config.get_osm_url(country=country),
            country_iso2=config.get_iso2(country=country),
            schema_filename=config.get_osm_rail_tags_schema(country=country),
            osm_output_filename=config.get_osm_rail_raw_osm(country=country),
            gpkg_output_filename=config.get_osm_rail_raw_gpkg(country=country),
            dag=dag
        )

        source = "osm"
        rail_transform = OSMRailTransformOperator(
            task_id=f"{country}_osm_rail_transform",
            source=source,
            input_filename=config.get_osm_rail_raw_gpkg(country=country),
            output_filename=config.get_osm_rail_processed_filepath(country=country),
            crs=config.get_crs(),
            schema_mapping=config.get_rail_schema_mapping(source=source, country=country),
            dag=dag
        )

        osm_rail_extract >> rail_transform
    return dag
