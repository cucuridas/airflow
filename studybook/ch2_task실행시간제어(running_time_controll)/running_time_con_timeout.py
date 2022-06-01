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

with DAG(
    default_args=default_args,
    dag_id='running_controller_timeout',
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,   
    tags=['example', 'example2'],
    params={"example_key": "example_value"},
    dagrun_timeout=datetime.timedelta(seconds=5)   
) as dag:

    test_c = BashOperator(
        owner="chung",
        task_id="pr_test112",
        bash_command="echo '{{ti.try_number}}' && sleep 10",
        #해당 task를 통해 task running time에 대한 제한이 이루어짐
        execution_timeout=datetime.timedelta(seconds=5)
    )

    test_d = BashOperator(
        owner="chung",
        task_id="pr_test1113",
        bash_command="echo '{{ti.try_number}}' && sleep 3"
    )    
    

    pr_f = BashOperator(
        owner="choi",
        task_id="pr_test1",
        retries=3,
        retry_delay=datetime.timedelta(seconds=10),
        bash_command="echo '{{ti.try_number}}' && sleep 8"

    )

    pr_d = BashOperator(
        owner="choi",
        task_id="pr_test2",
        retries=3,
        retry_delay=datetime.timedelta(seconds=10),       
        bash_command="echo '{{ti.try_number}}' && sleep 15"
   

    )

    pr_e = BashOperator(
        owner="choi",
        task_id="pr_test3",
        retries=3,
        retry_delay=datetime.timedelta(seconds=10),
        bash_command="echo '{{ti.try_number}}' && sleep 8"
    )

    ffd = EmptyOperator(
        task_id='pr_test44',
    )        


    cross_downstream([test_c,test_d],[pr_f,pr_d,pr_e])
    [pr_f,pr_d,pr_e] >> ffd