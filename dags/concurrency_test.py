import datetime

import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.helpers import cross_downstream

with DAG(
    dag_id='concurrency_test',
    schedule_interval='0 0 * * *',
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    dagrun_timeout=datetime.timedelta(minutes=60),
    tags=['example', 'example2'],
    params={"example_key": "example_value"},
) as dag:

    extract_a = BashOperator(
        owner="chung",
        task_id="extract_a",
        wait_for_downstream= True,
        bash_command="echo '{{ti.try_number}}' && sleep 3"
    )

    extract_b = BashOperator(
        owner="chung",
        task_id="extract_b",
        wait_for_downstream= True,
        bash_command="echo '{{ti.try_number}}' && sleep 3"
    )    
    

    process_a = BashOperator(
        owner="choi",
        task_id="process_a",
        retries=3,
        retry_delay=datetime.timedelta(seconds=10),
        bash_command="echo '{{ti.try_number}}' && sleep 8",
        pool="test_pool"

    )

    process_b = BashOperator(
        owner="choi",
        task_id="process_b",
        retries=3,
        retry_delay=datetime.timedelta(seconds=10),
        bash_command="echo '{{ti.try_number}}' && sleep 8",
        pool="test_pool"
   

    )

    process_c = BashOperator(
        owner="choi",
        task_id="process_c",
        retries=3,
        retry_delay=datetime.timedelta(seconds=10),
        bash_command="echo '{{ti.try_number}}' && sleep 8",
        pool="test_pool"      

    )

    sorkd = EmptyOperator(
        task_id='sorkd',
    )        


    cross_downstream([extract_a,extract_b],[process_a,process_b,process_c])
    [process_a,process_b,process_c] >> sorkd