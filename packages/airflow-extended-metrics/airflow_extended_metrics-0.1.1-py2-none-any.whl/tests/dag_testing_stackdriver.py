from datetime import datetime, timedelta

from airflow.operators.bash_operator import BashOperator
from airflow import DAG
from airflow.macros.monitor_test import monitor_operator, monitor


default_args = {
    'owner': 'extensions',
    'depends_on_past': False,
    'start_date': datetime(2019, 1, 1),
    'email': ['extensions@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'catchup': False,
    'schedule_interval': None
}

dag = DAG('custom_metrics', default_args=default_args)


bash = monitor_operator(BashOperator(
    task_id='echo_bash',
    bash_command='echo hello',
    dag=dag
), "nytdata", "us-central1")

bash
