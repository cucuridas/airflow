from datetime import datetime
from logging import Logger, log
from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.trigger_dagrun import TriggerDagRunOperator



dag = DAG(
        dag_id='original_Task',
        description='Compound Task to work',
        schedule_interval='0 12 * * *',
        start_date=datetime(2017, 3, 20), catchup=False,
        tags=["trigger"]
        )

t1 = TriggerDagRunOperator(
    trigger_dag_id= "crolling_TEXT_WF",
    task_id = "original_Task",
    wait_for_completion=True,
    dag=dag,
    reset_dag_run=True,
    poke_interval=30
)


t2 = TriggerDagRunOperator( 
    trigger_dag_id= "Finde_keyword_WF",
    task_id = "original_Task2",
    wait_for_completion=True,
    dag=dag,
    reset_dag_run=True,
    poke_interval=30
)

t1 >> t2