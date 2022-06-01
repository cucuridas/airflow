# Airflow TASK running time 관리를 위한 설정

Airflow에서는 task 처리에 대한 시간이 consumer(contents를 사용하고 소비하는 사람)의 기준보다 많이 소요가 됬었을 경우가 빈번히 발생한다 예를 들어 데이터 log를 전처리하는 작업을 진행하는데 log의 길이가 길어질수록 시간이 늘어나고 그에 따른 computing resource 가 점유하고 있는 시간들도 늘어나게 된다 이에 따라 task의 'running time'에 대해 제어 할 수 있는 설정이 존재하는데 SLA 과 Time Out 에 대한 설정이다

* sla란? - 기본적인 개념은 service-level Agreement의 약자로서 consumer의 서비스 수준을 기술한 문서를 의미하지만 Airflow는 consumer가 바라는 running time 에 대한 요구치라고 정의할 수 있다


### Airflow 에서의 'SLA' 와 'Time Out'의 차이점

큰 차이점으로 보았을 때 SLA는 진행 중인 task가 임계치에 진행 되었을 때 해당 task에 대한 표기 진행 및 이메일로 해당 task 내용에 대한 정보를 제공하는것이며, Time out은 task를 종료하여 사용중인 resource를 반납한다
또 SLA 경우 dag argument 설정이 python function 을 호출하는 함으로 여러가지 액션을 정의하고 호출 할 수 있다.

||SLA|Time out|
|------|---|---|
|Task 계속 진행|O|X|
|Action에 대한 가변성|O|X|
|자원 점유 여부|O|X|

위의 표를 정리하면서 "Time out 쓰지말고 SLA 쓰면 되지않을까?"라고 생각했지만 무분별한 SLA는 zombie task를 만들어 내고 resource를 계속 점유함으로 인해 Airflow 자체의 성능저하의 원인이 된다고 한다 방금 말한 얘기가 확 와닫지 않을 것 같아 예시를 하나 들자면 하나의 task가 resource를 할당 받고 진행 중이다 하지만 이 작업이 영원히 끝나지 않는 "PI(원주율 값)" 대한 계산하다고 가정했을 때 해당 task는 resource 계속 점유하게 되고 앞서 말한 예시의 task가 많아질수록 Airflow의 성능을 저하시키는 요인이 될 것이다 이러한 문제 때문에 SLA의 설정을 고려해야하는 까닭이다

### SLA 설정 방법

SLA 설정은 DAG 내부에서 이루어 지게 되는데 간단하게 요약하자면

* python function 으로 되어진 규격에 맞춰 정의
* DAG에서 callback 할 function 지정 
* task에서 임계치(일정 시간 이후) 지정

로 이루어 지게 된다

* python function 정의 부분

```python
#호출 되는 dag,task_list,blocking_task_list, slas, blocking_tis 를 파라미터로 받아와 함수 호출 
def print_sla_miss(dag, task_list, blocking_task_list, slas, blocking_tis):
    # dag 정보와 slas 정보를 log로 출력
    print (f'SLAs for dag : {dag} - SLAs: {slas}')
```

* DAG, TASK 인스턴스 생성 시 "sla_miss_callback" 를 통해 정의 

```python
#sla가 발생 했을 경우 python function 'print_sla_miss'를 호출하고 task 'test_a'와 'pr_b'의 task가 10초 이상의 시간이 걸렸을 때 web-ui(Browse-Sla Miss)에 출력 되게끔 로직 작성
with DAG(
    default_args=default_args,
    dag_id='running_time_controll',
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
    
    pr_b = BashOperator(
        owner="choi",
        task_id="pr_b",
        retries=3,
        retry_delay=datetime.timedelta(seconds=10),
        sla=datetime.timedelta(seconds=10),        
        bash_command="echo '{{ti.try_number}}' && sleep 15",
        pool="test_pool"
   

    )
    
```
* web ui 에서 임계치를 넘은 task들에 대한 내용을 남긴다 * log를 남긴뒤에 남겨진 log를 화면에 불러옴으로 ui에서 나타나는 시간이 지연될 수 있음
![image](https://user-images.githubusercontent.com/65060314/171296947-9d93f1fc-4b70-4ca9-beea-e9e1056ce2f0.png)

### Time out 설정 방법 

#### * DAG Time out 설정 방법 - DAG 작성 시  "dagrun_timeout" argument를 통해서 설정 가능

```python
#DAG가 실행 된 뒤 5초의 running time 이 지날 경우 DAG를 fail 처리
with DAG(
    default_args=default_args,
    dag_id='running_controller_timeout',
    schedule_interval='0 0 * * *',
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,   
    tags=['example', 'example2'],
    params={"example_key": "example_value"},
    #아래 argument를 통해 time out 설정 가능
    dagrun_timeout=datetime.timedelta(seconds=5)    
) as dag:

    test_c = BashOperator(
        owner="chung",
        task_id="test_c",
        wait_for_downstream= True,
        bash_command="echo '{{ti.try_number}}' && sleep 10"
    )
```

* 5초 후 해당 DAG가 '실패' 처리되는 모습

![airflow_guide_image](https://user-images.githubusercontent.com/65060314/171298662-adb26b55-0208-43d2-a820-c91a73430a33.gif)

<img width="473" alt="image" src="https://user-images.githubusercontent.com/65060314/171299138-1828ddaa-64cd-4587-b787-8d793e9cef4a.png">


#### * Task Time out 설정 방법 - Task 정의 시 'execution_timeout'옵션을 통해 지정 가능

```python
with DAG(
    default_args=default_args,
    dag_id='running_controller_timeout',
    schedule_interval='0 0 * * *',
    start_date=pendulum.datetime(2021, 1, 1, tz="UTC"),
    catchup=False,   
    tags=['example', 'example2'],
    params={"example_key": "example_value"}   
) as dag:
    test_c = BashOperator(
        owner="chung",
        task_id="pr_test112",
        wait_for_downstream= True,
        bash_command="echo '{{ti.try_number}}' && sleep 10",
        execution_timeout=datetime.timedelta(seconds=5)
    )
```

* 설정해둔 task의 작업이 5초이상 진행 될 경우 실패 처리  - 실패된 항목이 다른 task의 upstream 관련 의존성을 가질경우 실패 된 task 이후의 작업은 진행되지 않음

![airflow_guide_image2](https://user-images.githubusercontent.com/65060314/171396213-ec671c24-a2a5-462a-ba17-e11f52a0aa6b.gif)


<img width="538" alt="image" src="https://user-images.githubusercontent.com/65060314/171396777-65a74595-9513-4c1e-ac31-b91de2d31575.png">



```python

```


```python

```
