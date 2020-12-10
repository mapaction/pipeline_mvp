from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta

from airflow.operators.pipeline_plugin import HDXExtractOperator, HDXRoadsTransformOperator


def create_hdx_road_dag(country, schedule_interval, catchup, config, default_args):
    dag = DAG(f"{country}_hdx_road", schedule_interval=schedule_interval, catchup=catchup, default_args=default_args)
    
    hdx_roads_extract = HDXExtractOperator(
        task_id=f"{country}_hdx_roads_extract",
        hdx_address=config.get_hdx_roads_address(country=country),
        hdx_filename=config.get_hdx_roads_filename(country=country),
        save_directory="test",
        dag=dag
    )
    roads_transform = HDXRoadsTransformOperator(
        task_id=f"{country}_hdx_roads_transform",
        input_filename="/opt/data/test/ymn-roads.zip",
        schema_filename="/usr/local/airflow/plugins/pipeline_plugin/schemas/roads_affected_area_py.yml",
        output_filename="/opt/data/test/yem_tran_rds_ln_s1_ocha_pp.shp",
        schema_mapping=config.get_roads_schema_mapping(source="hdx"),
        crs=config.get_crs(),
        dag=dag
    )

    hdx_roads_extract >> roads_transform
    return dag
