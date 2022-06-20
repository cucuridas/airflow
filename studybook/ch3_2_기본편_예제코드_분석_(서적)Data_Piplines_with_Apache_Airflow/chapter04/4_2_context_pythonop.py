import airflow.utils.dates
from airflow import DAG
from airflow.operators.python import PythonOperator

dag = DAG(
    dag_id="4_2_context_pythonop",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="@once",
)


def _print_context(**context):
    print(context)


print_context = PythonOperator(
    task_id="print_context", python_callable=_print_context, dag=dag
)
