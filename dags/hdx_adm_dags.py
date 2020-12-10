from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta

from airflow.operators.pipeline_plugin import HDXExtractOperator, HDXAdm0Operator, HDXAdm1Operator


def create_hdx_adm0_dag(country, schedule_interval, catchup, config, default_args):
    dag = DAG(f"hdx_adm_{country}", schedule_interval=schedule_interval, catchup=catchup, default_args=default_args)

    hdx_extract = HDXExtractOperator(
        task_id=f"hdx_adm0_{country}_extract",
        country=country,
        config=config,
        hdx_address=config.get_hdx_adm_address(country=country),
        hdx_filename=config.get_hdx_adm_filename(country=country),
        dag=dag
    )
    adm0_transform = HDXAdm0Operator(
        task_id=f"hdx_adm0_{country}_transform",
        source='cod',
        adm_level='adm0',
        input_filename="/opt/data/test/yem_adm_govyem_cso_ochayemen_20191002_GPKG.zip",
        schema_filename="/usr/local/airflow/plugins/pipeline_plugin/schemas/admin0_affected_area_py.yml",
        output_filename="/opt/data/test/yem_adm0_processed.zip",
        iso3=config.get_iso3(country),
        raw_data_dir=config.get_dir_raw_data(),
        geoboundaries_adm0_raw=config.get_geoboundaries_adm0_raw(),
        schema_mapping=config.get_adm0_schema_mapping(source='cod'),
        crs=config.get_crs(),
        gadm_layer=config.get_gadm_layer_adm0(),
        dag=dag
    )

    adm1_transform = HDXAdm1Operator(
        task_id=f"hdx_adm1_{country}_transform",
        source="cod",
        adm_level='adm1',
        input_filename="/opt/data/test/yem_adm_govyem_cso_ochayemen_20191002_GPKG.zip",
        schema_filename="/usr/local/airflow/plugins/pipeline_plugin/schemas/admin1_affected_area_py.yml",
        output_filename="/opt/data/test/yem_adm1_processed.zip",
        iso3=config.get_iso3(country=country),
        raw_data_dir=config.get_dir_raw_data(),
        geoboundaries_adm1_raw=config.get_geoboundaries_adm1_raw(),
        schema_mapping=config.get_adm1_schema_mapping(source="cod"),
        crs=config.get_crs(),
        gadm_layer=config.get_gadm_layer_adm1(),
        dag=dag
    )

    hdx_extract >> [adm0_transform, adm1_transform]
    return dag
