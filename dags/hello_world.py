from airflow import DAG
from airflow.operators import BashOperator
from datetime import datetime, timedelta

from utils.default_args import get_default_arguments

# Following are defaults which can be overridden later on
default_args = get_default_arguments()

dag = DAG('Helloworld', default_args=default_args)

t1 = BashOperator(
    task_id='task_1',
    bash_command='echo "Hello MapAction"',
    dag=dag)

t2 = BashOperator(
    task_id='task_2',
    bash_command='echo "Hello Digital Power"',
    dag=dag)

t3 = BashOperator(
    task_id='task_3',
    bash_command='ls /data',
    dag=dag)

t1 >> t2 >> t3