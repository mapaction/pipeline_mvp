from airflow import DAG

from airflow.operators.pipeline_plugin import (OSMExtractOperator,
                                               OSMSeaportsTransformOperator)
from utils.config_parser import config
from utils.dag_configuration import (get_catchup, get_default_arguments,
                                     get_schedule_interval)

countries = config.get_countries()

# Defaults which can be overridden if needed
default_args = get_default_arguments()
schedule_interval = get_schedule_interval()
catchup = get_catchup()

with DAG(
    "osm_seaports",
    schedule_interval=schedule_interval,
    catchup=catchup,
    default_args=default_args,
) as dag:
    for country in countries:
        osm_seaports_extract = OSMExtractOperator(
            task_id=f"{country}_osm_seaports_extract",
            osm_url=config.get_osm_url(country=country),
            country_iso2=config.get_iso2(country=country),
            schema_filename=config.get_osm_seaports_tags_schema(country=country),
            osm_output_filename=config.get_osm_seaports_raw_osm(country=country),
            gpkg_output_filename=config.get_osm_seaports_raw_gpkg(country=country),
            dag=dag,
        )

        source = "osm"
        seaports_transform = OSMSeaportsTransformOperator(
            task_id=f"{country}_osm_seaports_transform",
            source=source,
            input_filename=config.get_osm_seaports_raw_gpkg(country=country),
            output_filename=config.get_osm_seaports_processed_filepath(country=country),
            crs=config.get_crs(),
            schema_mapping=config.get_seaports_schema_mapping(
                source=source, country=country
            ),
            dag=dag,
        )

        osm_seaports_extract >> seaports_transform
