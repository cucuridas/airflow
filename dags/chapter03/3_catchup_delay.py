import datetime as dt
from airflow import DAG
from airflow.operators.bash_operator import BashOperator


with DAG(
    dag_id='3_catchup_delay',
    #schedule_interval=dt.timedelta(sechonds=4),
    start_date=dt.datetime(year=2019, month=1, day=1),
    end_date=dt.datetime(year=2019, month=1, day=5),
    catchup=True,
    tags=['example', 'example2']
) as dag:
    test_task1 = BashOperator(task_id="test_task1",bash_command=("sleep 5"))

    test_task2 = BashOperator(task_id='test_task2',bash_command=("echo 'It is done'"))


    test_task1 >> test_task2