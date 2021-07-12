from airflow import DAG

from airflow.operators.pipeline_plugin import (
    OSMExtractOperator,
    OSMPlacesTransformOperator,
)
from utils.config_parser import config
from utils.dag_configuration import (
    get_catchup,
    get_default_arguments,
    get_schedule_interval,
)

countries = config.get_countries()

# Defaults which can be overridden if needed
default_args = get_default_arguments()
schedule_interval = get_schedule_interval()
catchup = get_catchup()

with DAG(
    "osm_places",
    schedule_interval=schedule_interval,
    catchup=catchup,
    default_args=default_args,
) as dag:
    for country in countries:
        osm_places_extract = OSMExtractOperator(
            task_id=f"{country}_osm_places_extract",
            osm_url=config.get_osm_url(country=country),
            country_iso2=config.get_iso2(country=country),
            overpass_query_schema_filename=config.get_osm_query_schema(
                country=country, dataset_name="places"
            ),
            osm_output_filename=config.get_raw_osm_data_path(
                country=country, dataset_name="places", format="raw_osm"
            ),
            gpkg_output_filename=config.get_raw_osm_data_path(
                country=country, dataset_name="places", format="raw_gpkg"
            ),
            dag=dag,
        )

        source = "osm"
        places_transform = OSMPlacesTransformOperator(
            task_id=f"{country}_osm_places_transform",
            source=source,
            input_filename=config.get_raw_osm_data_path(
                country=country, dataset_name="places", format="raw_gpkg"
            ),
            output_filename=config.get_osm_processed_filepath(
                country=country, dataset_name="places"
            ),
            crs=config.get_crs(),
            schema_mapping=config.get_schema_mapping(
                source=source, country=country, dataset_name="places"
            ),
            dag=dag,
        )

        osm_places_extract >> places_transform
