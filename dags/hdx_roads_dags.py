from airflow import DAG

from airflow.operators.pipeline_plugin import (
    HDXExtractOperator,
    HDXRoadsTransformOperator,
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
    "hdx_road",
    schedule_interval=schedule_interval,
    catchup=catchup,
    default_args=default_args,
) as dag:
    for country in countries:
        if config.should_process_hdx_roads(country):
            hdx_roads_extract = HDXExtractOperator(
                task_id=f"{country}_hdx_roads_extract",
                hdx_address=config.get_hdx_roads_address(country=country),
                hdx_filename=config.get_hdx_roads_dataset_name(country=country),
                output_filename=config.get_roads_cod_raw_filename(country=country),
                dag=dag,
            )
            source = "cod"
            roads_transform = HDXRoadsTransformOperator(
                task_id=f"{country}_hdx_roads_transform",
                source=source,
                input_filename=config.get_roads_cod_raw_filename(country=country),
                output_filename=config.get_roads_cod_processed_filepath(
                    country=country
                ),
                schema_mapping=config.get_roads_schema_mapping(
                    source=source, country=country
                ),
                crs=config.get_crs(),
                dag=dag,
            )

            hdx_roads_extract >> roads_transform
