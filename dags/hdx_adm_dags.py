from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta

from airflow.operators.pipeline_plugin import HDXExtractOperator, HDXAdm0Operator, HDXAdm1Operator


def create_hdx_adm0_dag(country, schedule_interval, catchup, config, default_args):
    dag = DAG(f"hdx_adm0_{country}", schedule_interval=schedule_interval, catchup=catchup, default_args=default_args)
    
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
        country=country,
        config=config,
        dag=dag
    )

    adm1_transform = HDXAdm1Operator(
        task_id=f"hdx_adm1_{country}_transform",
        country=country,
        config=config,
        dag=dag
    )

    # hdx_extract >> adm0_transform
    hdx_extract >> [adm0_transform, adm1_transform]
    return dag
