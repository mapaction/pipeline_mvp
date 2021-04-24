from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta
from country_config import config

from airflow.operators.pipeline_plugin import HDXExtractOperator, HDXRoadsTransformOperator


def create_hdx_road_dag(countries, schedule_interval, catchup, default_args):
    dag = DAG(f"hdx_road", schedule_interval=schedule_interval, catchup=catchup, default_args=default_args)
    
    for country in countries:
        if config.should_process_hdx_roads(country):
            hdx_roads_extract = HDXExtractOperator(
                task_id=f"{country}_hdx_roads_extract",
                hdx_address=config.get_hdx_roads_address(country=country),
                hdx_filename=config.get_hdx_roads_dataset_name(country=country),
                output_filename=config.get_roads_cod_raw_filename(country=country),
                dag=dag
            )
            source = "cod"
            roads_transform = HDXRoadsTransformOperator(
                task_id=f"{country}_hdx_roads_transform",
                source=source,
                input_filename=config.get_roads_cod_raw_filename(country=country),
                output_filename=config.get_roads_cod_processed_filepath(country=country),
                schema_mapping=config.get_roads_schema_mapping(source=source, country=country),
                crs=config.get_crs(),
                dag=dag
            )

            hdx_roads_extract >> roads_transform
    return dag
