from airflow.operators.pipeline_plugin import (
    DefaultTransformOperator,
    OSMExtractOperator,
)
from dags.dags_utils.dag_configuration import get_dags_configuration


def fill_osm_dag(dag, config, dataset_name: str, country: str):
    dags_config = get_dags_configuration()
    transform = dags_config["osm"][dataset_name]["transform"]
    osm_extract = OSMExtractOperator(
        task_id=f"{country}_osm_{dataset_name}_extract",
        osm_url=config.get_osm_url(country=country),
        country_iso2=config.get_iso2(country=country),
        overpass_query_schema_filename=config.get_osm_query_schema(
            country=country, dataset_name=dataset_name
        ),
        osm_output_filename=config.get_raw_osm_data_path(
            country=country, dataset_name=dataset_name, format="raw_osm"
        ),
        gpkg_output_filename=config.get_raw_osm_data_path(
            country=country, dataset_name=dataset_name, format="raw_gpkg"
        ),
        dag=dag,
    )

    source = "osm"
    osm_transform = DefaultTransformOperator(
        task_id=f"{country}_osm_{dataset_name}_transform",
        source=source,
        input_filename=config.get_raw_osm_data_path(
            country=country, dataset_name=dataset_name, format="raw_gpkg"
        ),
        output_filename=config.get_osm_processed_filepath(
            country=country, dataset_name=dataset_name
        ),
        crs=config.get_crs(),
        schema_mapping=config.get_schema_mapping(
            source=source, country=country, dataset_name=dataset_name
        ),
        transform_method=transform,
        dag=dag,
    )

    osm_extract >> osm_transform
