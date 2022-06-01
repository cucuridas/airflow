import datetime
from email.policy import default

import pendulum

from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from airflow.utils.helpers import cross_downstream

default_args = {
    "email_on_failure": False
}

def print_sla_miss(dag, task_list, blocking_task_list, slas, blocking_tis):
    print (f'SLAs for dag : {dag} - SLAs: {slas}')

with DAG(
    default_args=default_args,
    dag_id='running_controller_sla',
    schedule_interval='*/2 * * * *',
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,
    sla_miss_callback=print_sla_miss,    
    tags=['example', 'example2'],
    params={"example_key": "example_value"},
) as dag:

    test_a = BashOperator(
        owner="chung",
        task_id="test_a",
        wait_for_downstream= True,
        bash_command="echo '{{ti.try_number}}' && sleep 10",
        sla=datetime.timedelta(seconds=5)
    )

    test_b = BashOperator(
        owner="chung",
        task_id="test_b",
        wait_for_downstream= True,
        bash_command="echo '{{ti.try_number}}' && sleep 3"
    )    
    

    pr_a = BashOperator(
        owner="choi",
        task_id="pr_a",
        retries=3,
        retry_delay=datetime.timedelta(seconds=10),
        bash_command="echo '{{ti.try_number}}' && sleep 8",
        pool="test_pool"

    )

    pr_b = BashOperator(
        owner="choi",
        task_id="pr_b",
        retries=3,
        retry_delay=datetime.timedelta(seconds=10),
        sla=datetime.timedelta(seconds=10),        
        bash_command="echo '{{ti.try_number}}' && sleep 15",
        pool="test_pool"
   

    )

    pr_c = BashOperator(
        owner="choi",
        task_id="pr_c",
        retries=3,
        retry_delay=datetime.timedelta(seconds=10),
        bash_command="echo '{{ti.try_number}}' && sleep 8",
        pool="test_pool"      

    )

    ddf = EmptyOperator(
        task_id='ddf',
    )        


    cross_downstream([test_a,test_b],[pr_a,pr_b,pr_c])
    [pr_a,pr_b,pr_c] >> ddf