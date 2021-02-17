from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta
import os

from airflow.operators.pipeline_plugin import HDXExtractOperator, HDXAdm0TransformOperator, HDXAdm1TransformOperator, RCloneOperator
from config import config

def create_hdx_adm_dag(countries, schedule_interval, catchup, default_args):
    dag = DAG(f"hdx_adm", schedule_interval=schedule_interval, catchup=catchup, default_args=default_args)

    for country in countries:
        hdx_extract = HDXExtractOperator(
            task_id=f"{country}_hdx_adm_extract",
            hdx_address=config.get_hdx_adm_address(country=country),
            hdx_filename=config.get_hdx_adm_dataset_name(country=country),
            output_filename=os.path.join(dag.dag_id, country, config.get_adm_cod_raw_filename(country=country)),
            dag=dag
        )

        source = "cod"
        adm0_transform = HDXAdm0TransformOperator(
            task_id=f"{country}_hdx_adm0_transform",
            source=source,
            adm_level='adm0',
            input_filename=os.path.join(dag.dag_id, country, config.get_adm_cod_raw_filename(country=country)),
            input_file_type=config.get_hdx_adm_dataset_type(country=country),
            input_layer_name=config.get_hdx_adm0_dataset_layer_name(country=country),
            schema_filename=config.get_adm0_schema(country=country),
            output_filename=os.path.join(dag.dag_id, country, config.get_adm0_cod_processed_filepath(country=country)),
            iso3=config.get_iso3(country=country),
            source_geoboundaries=config.get_geoboundaries_adm0_raw(),
            schema_mapping=config.get_adm0_schema_mapping(source=source, country=country),
            crs=config.get_crs(),
            gadm_layer=config.get_gadm_layer_adm0(),
            dag=dag
        )

        adm1_transform = HDXAdm1TransformOperator(
            task_id=f"{country}_hdx_adm1_transform",
            source=source,
            adm_level='adm1',
            input_filename=os.path.join(dag.dag_id, country, config.get_adm_cod_raw_filename(country=country)),
            input_file_type=config.get_hdx_adm_dataset_type(country=country),
            input_layer_name=config.get_hdx_adm1_dataset_layer_name(country=country),
            schema_filename=config.get_adm1_schema(country=country),
            output_filename=os.path.join(dag.dag_id, country, config.get_adm1_cod_processed_filepath(country=country)),
            iso3=config.get_iso3(country=country),
            source_geoboundaries=config.get_geoboundaries_adm1_raw(),
            schema_mapping=config.get_adm1_schema_mapping(source=source, country=country),
            crs=config.get_crs(),
            gadm_layer=config.get_gadm_layer_adm1(),
            dag=dag
        )

        hdx_extract >> [adm0_transform, adm1_transform]

    sync_operator = RCloneOperator(
        task_id=f"all_countries_sync_data",
        dag=dag
    )
    return dag
