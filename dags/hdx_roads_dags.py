from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta

from airflow.operators.pipeline_plugin import HDXExtractOperator, RoadsTransformOperator


def create_road_dag(country, geo_extent, schedule_interval, catchup, config, default_args):
    dag = DAG(f"road_{country}", schedule_interval=schedule_interval, catchup=catchup, default_args=default_args)
    
    hdx_roads_extract = HDXExtractOperator(
        task_id=f"adm0_{country}_extract",
        country=country,
        config=config,
        hdx_address=config.get_hdx_roads_address(country=country),
        hdx_filename=config.get_hdx_roads_filename(country=country),
        dag=dag
    )
    roads_transform = RoadsTransformOperator(
        task_id=f"adm0_{country}_transform",
        country=country,
        config=config,
        dag=dag
    )

    hdx_roads_extract >> roads_transform
    return dag
