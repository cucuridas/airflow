from datetime import datetime

import pandas as pd
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.operators.dummy import DummyOperator

dag = DAG(
    dag_id="3_1_dummy_scheduled",
    schedule_interval="@daily",
    start_date=datetime(2019, 1, 1),
    end_date=datetime(2019, 1, 5),
)

task1 = DummyOperator(task_id="dummy1" ,dag=dag)

task2 = DummyOperator(task_id="dummy2", dag=dag)


task1 >> task2