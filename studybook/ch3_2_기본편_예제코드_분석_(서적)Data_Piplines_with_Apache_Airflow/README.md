책의 예제 DAG를 통한 코드 리뷰 
-----
### 요약  
1) 2장 Airflow DAG 구조 - download_rocket_lunches  
2) 3장 Airflow Scheduled  
3) 4장 Jinja-template  
4) 5장 branch xcom

##  1) 2장 Airflow DAG 구조

### dag 를 정의 하는 부분
- dag_id,start_date,scheduler_interval에 대한 값 미지정 시 compile error로 인해 UI에서 해당 DAG를 확인할 수 없음

- error ui 첨부 필요 이미지 추가 필요


```python
dag = DAG(
    dag_id="download_rocket_launches",
    description="Download rocket pictures of recently launched rockets.",
    start_date=airflow.utils.dates.days_ago(14),
    schedule_interval="@daily",
)
```

### task를 정의하는 부분

* bash operator를 사용한 task 정의
* business logic : 로켓에 대한 최신 이미지를 받을 수 있도록 만든 api 서버에서 이미지 url 정보를 받아와 /tmp/launches.json 파일에 저장하는 작업을 진행



```python
download_launches = BashOperator(
    task_id="download_launches",
    bash_command="curl -o /tmp/launches.json -L 'https://ll.thespacedevs.com/2.0.0/launch/upcoming'",  # noqa: E501
    dag=dag,
)
```

* python operator를 사용한 task 정의 - 'python_callable'의 값을 DAG 작성자가 정의한 함수의 이름으로 받아 해당 함수를 실행
* 모든 operator는 baseoperator를 사용받아 class로 정의하게 됨  
https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/baseoperator/index.html


```python
get_pictures = PythonOperator(
    task_id="get_pictures", python_callable=_get_pictures, dag=dag
)
```

* python 함수 내용
* business logic :  
     1- pathlib 라이브러리를 사용하여 /tmp/images라는 디렉토리가 있는지 확인하고 없으면 생성  
     2- /temp/launches.json 파일의 내용을 읽어와 메모리에 저장하여 필요한 정보를 파싱  
     3- request 라이브러리를 사용하여 image_url 정보로 이미지 데이터 다운로드하여 temp/images/ 디렉토리 하위에 저장  


```python
def _get_pictures():
    # Ensure directory exists
    pathlib.Path("/tmp/images").mkdir(parents=True, exist_ok=True)

    # Download all pictures in launches.json
    with open("/tmp/launches.json") as f:
        launches = json.load(f)
        image_urls = [launch["image"] for launch in launches["results"]]
        for image_url in image_urls:
            try:
                response = requests.get(image_url)
                image_filename = image_url.split("/")[-1]
                target_file = f"/tmp/images/{image_filename}"
                with open(target_file, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded {image_url} to {target_file}")
            except requests_exceptions.MissingSchema:
                print(f"{image_url} appears to be an invalid URL.")
            except requests_exceptions.ConnectionError:
                print(f"Could not connect to {image_url}.")
```

* 의존성을 정의하는 부분 - right sheeft 기호를 통해 의존성 정의


```python
download_launches >> get_pictures >> notify
```

* sample 코드 원본 내용


```python
#사용하고자하는 모듈에대한 정보를 저장
import json
import pathlib

import airflow.utils.dates
import requests
import requests.exceptions as requests_exceptions
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

#DAG class를 통해 객체 생성 
#dag_id,start_date,scheduler_interval에 대한 값 미지정 시 compile error로 인해 UI에서 해당 DAG를 확인할 수 없음
dag = DAG(
    dag_id="download_rocket_launches",
    description="Download rocket pictures of recently launched rockets.",
    start_date=airflow.utils.dates.days_ago(14),
    schedule_interval="@daily",
)
#bash operator를 통해서 task를 정의 
#business logic : 로켓에 대한 최신 이미지를 받을 수 있도록 만든 api 서버에서 이미지 url 정보를 받아와 /tmp/launches.json 파일에 저장하는 작업을 진행
download_launches = BashOperator(
    task_id="download_launches",
    bash_command="curl -o /tmp/launches.json -L 'https://ll.thespacedevs.com/2.0.0/launch/upcoming'",  # noqa: E501
    dag=dag,
)

#python operator에서 호출하게 될 함수를 정의
#business logic : 
# 1- pathlib 라이브러리를 사용하여 /tmp/images라는 디렉토리가 있는지 확인하고 없으면 생성
# 2- /temp/launches.json 파일의 내용을 읽어와 메모리에 저장하여 필요한 정보를 파싱
# 3- request 라이브러리를 사용하여 image_url 정보로 이미지 데이터 다운로드하여 temp/images/ 디렉토리 하위에 저장
def _get_pictures():
    # Ensure directory exists
    pathlib.Path("/tmp/images").mkdir(parents=True, exist_ok=True)

    # Download all pictures in launches.json
    with open("/tmp/launches.json") as f:
        launches = json.load(f)
        image_urls = [launch["image"] for launch in launches["results"]]
        for image_url in image_urls:
            try:
                response = requests.get(image_url)
                image_filename = image_url.split("/")[-1]
                target_file = f"/tmp/images/{image_filename}"
                with open(target_file, "wb") as f:
                    f.write(response.content)
                print(f"Downloaded {image_url} to {target_file}")
            except requests_exceptions.MissingSchema:
                print(f"{image_url} appears to be an invalid URL.")
            except requests_exceptions.ConnectionError:
                print(f"Could not connect to {image_url}.")

#바로 위 코드블럭에서 정의한 python 함수를 실제로 동작시키는 Python operator를 정의하게됨
#모든 operator는 baseoperator를 사용받아 class로 정의하게 됨
#https://airflow.apache.org/docs/apache-airflow/stable/_api/airflow/models/baseoperator/index.html
get_pictures = PythonOperator(
    task_id="get_pictures", python_callable=_get_pictures, dag=dag
)

#앞선 task가 끝난뒤 작업이 정상적으로 종료되었다는 task를 실행
notify = BashOperator(
    task_id="notify",
    bash_command='echo "There are now $(ls /tmp/images/ | wc -l) images."',
    dag=dag,
)
#의존성을 rigtht sheeft 를 통해 명시하게 됨
download_launches >> get_pictures >> notify

```

## 2) 3장 Airflow Scheduled

### scheduld 방법

* crontab 형식을 통한 시점 기반 scheduled    
  <img width="651" alt="image" src="https://user-images.githubusercontent.com/65060314/174480265-a9eed1a7-4608-4b0b-85a5-e38a0b2964c3.png">


```python
dag = DAG(
    dag_id="02_daily_schedule",
    schedule_interval="@daily",
    start_date=datetime(2019, 1, 1),
    end_date=datetime(2019, 1, 5),
)
```

* timedelta 라이브러리를 활용한 빈도기반 설정


```python
dag = DAG(
    dag_id="04_time_delta",
    schedule_interval=dt.timedelta(days=3),
    start_date=dt.datetime(year=2019, month=1, day=1),
    end_date=dt.datetime(year=2019, month=1, day=5),
)
```

* sample code 원본 내용


```python
from datetime import datetime
from pathlib import Path

import pandas as pd
from airflow import DAG
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator

dag = DAG(
    dag_id="02_daily_schedule",
    schedule_interval="@daily",
    start_date=datetime(2019, 1, 1),
    end_date=datetime(2019, 1, 5),
)

# bash operator를 활용해서 작업을 진행
# business logic :
# 1. /data/events 디렉토리를 생성
# 2. 생성한 디렉토리에 events api를 통해 가져온 데이터를 json 파일로 저장(현재 api는 구현되어있지 않음)
fetch_events = BashOperator(
    task_id="fetch_events",
    bash_command=(
        "mkdir -p /data/events && "
        "curl -o /data/events.json http://events_api:5000/events"
    ),
    dag=dag,
)

#실제 작업에서 진행하게 되는 함수 내용
# business logic : 
# 1. input_path와 out_path를 입력 받아 함수 시작
# 2. pandas 모듈을 통해 json 파일을 pd 객체로 읽어옴
# 3. 날짜와 user 정보를 통해 통계 계산 실행
# 4. 입력 받은 out_path 로 디렉토리 생성 및 csv 파일 저장
def _calculate_stats(input_path, output_path):
    """Calculates event statistics."""

    events = pd.read_json(input_path)
    stats = events.groupby(["date", "user"]).size().reset_index()

    Path(output_path).parent.mkdir(exist_ok=True)
    stats.to_csv(output_path, index=False)

#python operator를 통해 calculate_stats 함수를 실행
#op_kwargs를 활용하여 호출하는 함수의 parameter를 key argument 형식으로 전달
calculate_stats = PythonOperator(
    task_id="calculate_stats",
    python_callable=_calculate_stats,
    op_kwargs={"input_path": "/data/events.json", "output_path": "/data/stats.csv"},
    dag=dag,
)
# 의존성 명시
fetch_events >> calculate_stats

```

# 3) 4장 Jinja-template

* airflow context variable 정보  
<img width="411" alt="image" src="https://user-images.githubusercontent.com/65060314/174481384-cd3bbdbe-531c-474a-a9c0-d6ecda54665c.png">  
<img width="417" alt="image" src="https://user-images.githubusercontent.com/65060314/174481402-15f9f7d7-1399-4986-9599-011994c9f491.png">  

* bash operator에서 jinja template을 사용하기
    - "{"(중괄호)를 두개 사용하여 jinja template 정의


```python
import airflow
from airflow import DAG
from airflow.operators.bash import BashOperator

dag = DAG(
    dag_id="listing_4_01",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="@hourly",
)
#bash operator를 통해 작업에 필요한 command line 정의
# business logic :
# 위키피디아 api를 활용하여 압축된 증분 데이터를 다운로드 - 위키피디아의 특정 페이지의 뷰에 대한 정보
# /tmp/wikipagebiews.gz라는 이름으로 저장
get_data = BashOperator(
    task_id="get_data",
    bash_command=(
        "curl -o /tmp/wikipageviews.gz "
        "https://dumps.wikimedia.org/other/pageviews/"
        #context에서 정의 되어 있는 excution_date를 통해 작업 시작 시간에 대한 렌더링 데이터를 파싱
        "{{ execution_date.year }}/"
        "{{ execution_date.year }}-{{ '{:02}'.format(execution_date.month) }}/"
        "pageviews-{{ execution_date.year }}"
        "{{ '{:02}'.format(execution_date.month) }}"
        "{{ '{:02}'.format(execution_date.day) }}-"
        "{{ '{:02}'.format(execution_date.hour) }}0000.gz"
    ),
    dag=dag,
)
```

* python operator 에서 template 정보를 사용하기
    - '**' 표시를 통해 kargs를 통해서 렌더링 데이터를 가져와서 사용할 수 있도록 파라미터로 받아옴

*  특정 variable을 사용하고 싶을 때 정의하는 방법 


```python
def _print_context2(**context):
    start = context["execution_date"]
    end = context["next_execution_date"]
    print(f"Start: {start}, end: {end}")
```

* 파라미터로 입력 받을 때 부터 특정 variable을 지정하고 가져오기


```python
def _print_context3(execution_date,next_execution_date,**context):
    start = execution_date
    end = next_execution_date
    print(f"Start: {start}, end: {end}")
```

* op_kwargs를 사용시에는 jinja template을 통해 렌더링 데이터 접근


```python
# 
def _get_data(year, month, day, hour, output_path, **_):
    url = (
        "https://dumps.wikimedia.org/other/pageviews/"
        f"{year}/{year}-{month:0>2}/pageviews-{year}{month:0>2}{day:0>2}-{hour:0>2}0000.gz"
    )
    request.urlretrieve(url, output_path)


get_data = PythonOperator(
    task_id="get_data",
    python_callable=_get_data,
    op_kwargs={
        "year": "{{ execution_date.year }}",
        "month": "{{ execution_date.month }}",
        "day": "{{ execution_date.day }}",
        "hour": "{{ execution_date.hour }}",
        "output_path": "/tmp/wikipageviews.gz",
    },
    dag=dag,
)
```

* sample code 원본 내용


```python
import airflow.utils.dates
from airflow import DAG
from airflow.operators.python import PythonOperator

dag = DAG(
    dag_id="listing_4_07",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="@daily",
)

# context라고 명시해둔 파라미터는 따로 사용자에 의해 정해진 이름
# '**' 라는 부분이 kwargs를 정의하는 부분 
def _print_context(**context):
    print(context)
# # 특정 variable을 사용하고 싶을 때 정의하는 방법    
# def _print_context2(**context):
#     start = context["execution_date"]
#     end = context["next_execution_date"]
#     print(f"Start: {start}, end: {end}")
# # 파라미터로 입력 받을 때 부터 특정 variable을 지정하고 가져오기
# def _print_context3(execution_date,next_execution_date,**context):
#     start = execution_date
#     end = next_execution_date
#     print(f"Start: {start}, end: {end}")
    

print_context = PythonOperator(
    task_id="print_context", python_callable=_print_context, dag=dag
)
```

## 4) 5장 branch 와 xcom


* python 함수 내부 로직에 의해서만 branch 되도록 정의


```python
# 분기 내용 : 따로 task 명시가 진행되지 않았으며, branch operator를 통한 task 작업으로 진행되지않았음으로 따로 worker를 할당 받고 
# 다른 task를 진행하는 형태가 아닌 함수가 if 구문을 통해 다른 함수를 호출하는 형태의 구조로 작업 진행
def _fetch_sales(**context):
    if context["execution_date"] < ERP_CHANGE_DATE:
        _fetch_sales_old(**context)
    else:
        _fetch_sales_new(**context)
        
with DAG(
    dag_id="02_branch_function",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="@daily",
) as dag:
    start = DummyOperator(task_id="start")
    #호출하고자하는 _fetch_sales 함수 정의
    fetch_sales = PythonOperator(task_id="fetch_sales", python_callable=_fetch_sales)
    clean_sales = PythonOperator(task_id="clean_sales", python_callable=_clean_sales)

    fetch_weather = DummyOperator(task_id="fetch_weather")
    clean_weather = DummyOperator(task_id="clean_weather")

    join_datasets = DummyOperator(task_id="join_datasets")
    train_model = DummyOperator(task_id="train_model")
    deploy_model = DummyOperator(task_id="deploy_model")
    #의존성 내용에서 분기되어 실행되는 다른 함수(_fetch_sales_old,_fetch_sales_new)에 대한 정의가 존재하지않음
    start >> [fetch_sales, fetch_weather]
    fetch_sales >> clean_sales
    fetch_weather >> clean_weather
    [clean_sales, clean_weather] >> join_datasets
    join_datasets >> train_model >> deploy_model
```

* python branch operator 를 사용해서 분기


```python
#분기 내용: branch operator에 의해 작업이 worker에게 할당 받은 후 실행 됨으로 return에서 다른 함수를 호출하지않고 함수의 정의된 명칭만 전달
# return으로 전달 받은 함수를 동작하기 위한 operator 정의가 필요
def _pick_erp_system(**context):
    if context["execution_date"] < ERP_CHANGE_DATE:
        return "fetch_sales_old"
    else:
        return "fetch_sales_new"


with DAG(
    dag_id="03_branch_dag",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="@daily",
) as dag:

    pick_erp_system = BranchPythonOperator(
        task_id="pick_erp_system", python_callable=_pick_erp_system
    )
    #분기로 인해 실행될 python operator 정의
    fetch_sales_old = PythonOperator(
        task_id="fetch_sales_old", python_callable=_fetch_sales_old
    )
    #분기로 인해 실행될 python operator 정의
    fetch_sales_new = PythonOperator(
        task_id="fetch_sales_new", python_callable=_fetch_sales_new
    )

#task로 작업을 정의해주었기에 의존성 역시 정의가 필요함
pick_erp_system >> [fetch_sales_old, fetch_sales_new]    
```

* sample code 원본 내용


```python
import airflow

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.python import PythonOperator

ERP_CHANGE_DATE = airflow.utils.dates.days_ago(1)

# branch operatro 사용 없이 함수 분기
def _fetch_sales(**context):
    if context["execution_date"] < ERP_CHANGE_DATE:
        _fetch_sales_old(**context)
    else:
        _fetch_sales_new(**context)


def _fetch_sales_old(**context):
    print("Fetching sales data (OLD)...")


def _fetch_sales_new(**context):
    print("Fetching sales data (NEW)...")


def _clean_sales(**context):
    if context["execution_date"] < airflow.utils.dates.days_ago(1):
        _clean_sales_old(**context)
    else:
        _clean_sales_new(**context)


def _clean_sales_old(**context):
    print("Preprocessing sales data (OLD)...")


def _clean_sales_new(**context):
    print("Preprocessing sales data (NEW)...")


with DAG(
    dag_id="02_branch_function",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="@daily",
) as dag:
    start = DummyOperator(task_id="start")

    #branch operator 없이 함수 분기
    fetch_sales = PythonOperator(task_id="fetch_sales", python_callable=_fetch_sales)

    clean_sales = PythonOperator(task_id="clean_sales", python_callable=_clean_sales)

    fetch_weather = DummyOperator(task_id="fetch_weather")
    clean_weather = DummyOperator(task_id="clean_weather")

    join_datasets = DummyOperator(task_id="join_datasets")
    train_model = DummyOperator(task_id="train_model")
    deploy_model = DummyOperator(task_id="deploy_model")
    
    start >> [fetch_sales, fetch_weather]
    fetch_sales >> clean_sales        
    fetch_weather >> clean_weather
    [clean_sales, clean_weather] >> join_datasets
    join_datasets >> train_model >> deploy_model    
    
    # branch operator를 활용한 분기    
#     start = DummyOperator(task_id="start")

#     pick_erp_system = BranchPythonOperator(
#         task_id="pick_erp_system", python_callable=_pick_erp_system
#     )

#     fetch_sales_old = PythonOperator(
#         task_id="fetch_sales_old", python_callable=_fetch_sales_old
#     )
#     clean_sales_old = PythonOperator(
#         task_id="clean_sales_old", python_callable=_clean_sales_old
#     )

#     fetch_sales_new = PythonOperator(
#         task_id="fetch_sales_new", python_callable=_fetch_sales_new
#     )
#     clean_sales_new = PythonOperator(
#         task_id="clean_sales_new", python_callable=_clean_sales_new
#     )

#     fetch_weather = DummyOperator(task_id="fetch_weather")
#     clean_weather = DummyOperator(task_id="clean_weather")



    
#     #brach operator 사용했을 시 의존성 정의
#     start >> [pick_erp_system, fetch_weather]
#     pick_erp_system >> [fetch_sales_old, fetch_sales_new]
#     fetch_sales_old >> clean_sales_old
#     fetch_sales_new >> clean_sales_new
#     fetch_weather >> clean_weather
#     [clean_sales_old, clean_sales_new, clean_weather] >> join_datasets
#     join_datasets >> train_model >> deploy_model    

```

* xcom 사용 방법


```python
def _train_model(**context):
    model_id = str(uuid.uuid4())
    context["task_instance"].xcom_push(key="model_id", value=model_id)


def _deploy_model(**context):
    model_id = context["task_instance"].xcom_pull(
        task_ids="train_model", key="model_id"
    )
    print(f"Deploying model {model_id}")
```
