import os

from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta

from airflow.operators.pipeline_plugin import OSMExtractOperator, OSMRoadsTransformOperator


def create_osm_road_dag(country, schedule_interval, catchup, config, default_args):
    dag = DAG(f"osm_roads_{country}", schedule_interval=schedule_interval, catchup=catchup, default_args=default_args)

    osm_roads_extract = OSMExtractOperator(
        task_id=f"osm_roads_{country}_extract",
        country=country,
        config=config,
        dag=dag
    )

    roads_transform = OSMRoadsTransformOperator(
        task_id=f"osm_roads{country}_transform",
        source='osm',
        input_filename=os.path.join(config.get_dir_raw_data(),
                                    config.get_osm_roads_raw_gpkg(country=country)),
        schema_filename=os.path.join(config.get_schema_directory(),
                                     config.get_roads_schema()),
        output_filename=os.path.join(config.get_dir_processed_data(),
                                     config.get_osm_roads_processed_filename(country=country)),
        crs=config.get_crs(),
        dag=dag
    )

    osm_roads_extract >> roads_transform
    return dag


