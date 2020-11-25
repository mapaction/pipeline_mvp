from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta

from airflow.operators.pipeline_plugin import HDXExtractOperator, Adm0Operator

from utils.default_args import get_default_arguments

# Following are defaults which can be overridden later on
default_args = get_default_arguments()

dag = DAG('Yemen', default_args=default_args)

t3 = HDXExtractOperator(
    task_id="yemen_extract",
    country="yemen",
    dag=dag
)

t4 = Adm0Operator(
    task_id="yemen_transform",
    country="yemen",
    dag=dag
)

t3 >> t4