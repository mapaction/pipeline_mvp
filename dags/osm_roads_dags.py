from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta

from airflow.operators.pipeline_plugin import OSMExtractOperator


def create_osm_road_dag(country, schedule_interval, catchup, config, default_args):
    dag = DAG(f"osm_roads_{country}", schedule_interval=schedule_interval, catchup=catchup, default_args=default_args)

    osm_roads_extract = OSMExtractOperator(
        task_id=f"osm_roads_{country}_extract",
        country=country,
        config=config,
        dag=dag
    )
    # roads_transform = RoadsTransformOperator(
    #     task_id=f"adm0_{country}_transform",
    #     country=country,
    #     config=config,
    #     dag=dag
    # )
    #
    # hdx_roads_extract >> roads_transform
    return dag
