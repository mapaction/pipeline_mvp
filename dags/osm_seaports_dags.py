from airflow import DAG

from airflow.operators.pipeline_plugin import (
    DefaultTransformOperator,
    OSMExtractOperator,
)
from pipeline_plugin.transform.seaports_transform import transform
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
            overpass_query_schema_filename=config.get_osm_query_schema(
                country=country, dataset_name="seaports"
            ),
            osm_output_filename=config.get_raw_osm_data_path(
                country=country, dataset_name="seaports", format="raw_osm"
            ),
            gpkg_output_filename=config.get_raw_osm_data_path(
                country=country, dataset_name="seaports", format="raw_gpkg"
            ),
            dag=dag,
        )

        source = "osm"
        seaports_transform = DefaultTransformOperator(
            task_id=f"{country}_osm_seaports_transform",
            source=source,
            input_filename=config.get_raw_osm_data_path(
                country=country, dataset_name="seaports", format="raw_gpkg"
            ),
            output_filename=config.get_osm_processed_filepath(
                country=country, dataset_name="seaports"
            ),
            crs=config.get_crs(),
            schema_mapping=config.get_schema_mapping(
                source=source, country=country, dataset_name="seaports"
            ),
            transform_method=transform,
            dag=dag,
        )

        osm_seaports_extract >> seaports_transform
