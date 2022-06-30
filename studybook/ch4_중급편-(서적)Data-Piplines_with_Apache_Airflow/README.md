# Trigger
  
```
1) Trigger 란?
2) FileSensor를 통한 Trigger
3) PythonSensor를 통한 Trigger
4) 다른 DAG tirrger 하기
5) 다른 DAG의 상태 값 폴링 하기
```

## 1) Trigger 란?
스케쥴 간격과는 다르게 특정 조건 또는 사용자가 직접 실행을 시키고자 할 때 사용할 수 있는 Airflow DAG 실행 기법 
pooling을 통해 입력받은 시간동안 확인작업을 진행 한다
  
* web UI 에서도 '플레이' 버튼을 통해서 실행 가능  

<img width="445" alt="image" src="https://user-images.githubusercontent.com/65060314/175840584-3898749a-c3de-4d3d-94a1-0a6f95aa0e64.png">
  
<img width="356" alt="image" src="https://user-images.githubusercontent.com/65060314/175841420-5c608595-2b94-4c15-90f4-375937191ca8.png">


## 2) FileSensor를 통한 Trigger
FileSensor는 오퍼레이터의 서브 클래스인 sensor의 도움을 받아 인수로 입력 받은 파일경로에 해당 파일이 존재하는지 여부를 판단하여 bool type의 return을 전달 한다   
  
```python
from airflow.sensors.filesystem import FileSensor
wait = FileSensor(
    task_id="wait_for_supermarket_1", filepath="/data/supermarket1/data.csv", dag=dag
)
```

## 3) PythonSensor를 통한 Trigger
FileSensor는 파일에 대한 여부만 판단하기에 확장하거나 다른 조건에 trigger를 하기에 힘든 점이 존재하는데 이러한 단점을 보완하는 역할을 하는 PythonSensor가 존재한다 
PythonSensor는 callable 인수로 함수의 이름을 입력 받고 bool type의 return을 전달한다   

```python
def _wait_for_supermarket(supermarket_id_):
    supermarket_path = Path("/data/" + supermarket_id_)
    data_files = supermarket_path.glob("data-*.csv")
    success_file = supermarket_path / "_SUCCESS"
    return data_files and success_file.exists()


wait_for_supermarket_1 = PythonSensor(
    task_id="wait_for_supermarket_1",
    python_callable=_wait_for_supermarket,
    op_kwargs={"supermarket_id": "supermarket1"},
    dag=dag,
)
```

* 주의 사항
눈덩이 효과: schedule interver의 값은 매일매일 실행되도록 설정해 두었지만 pythonSensor의 timeout은 일주일로 설정해 두어 많은 resource를 사용하게되는 현상
* 해결방안   
    1) 'Concurrency' 인수를 통한 DAG 실행 갯수 제어  
    2) sensor 클래스의 'poke' 인수 값을 통해 최대 task 제한  
    3) sensor 클래스의 'reschedule' 모드를 통해 대기 시간동안은 task 슬롯을 차지하지 않도록 설정  

 ## 4) 다른 DAG tirrger 하기   
 "TriggerDagRunOperator" 모듈을 통해 현재 DAG에서 다른 DAG를 호출 하도록 설정 할 수 있음 다른 DAG를 실행 시키기 위해서는 "trigger_dag_id" 인수의 값으로 실행 하고자하는 DAG의 이름을 넣어주어 실행 하게되며 trigger operator 에 의해 실행되는 task의 schedule_interval 인수 값은 필요로 하지 않는다  
 
### DAG1  
 
```python
dag1 = DAG(
    dag_id="listing_6_04_dag01",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval="0 16 * * *",
)

trigger_create_metrics_dag = TriggerDagRunOperator(
        task_id=f"trigger_create_metrics_dag_supermarket_{supermarket_id}",
        trigger_dag_id="listing_6_04_dag02",
        dag=dag1,
    ) 
```  
  
### DAG2    

```python
dag2 = DAG(
    dag_id="listing_6_04_dag02",
    start_date=airflow.utils.dates.days_ago(3),
    schedule_interval=None,
)
  
compute_differences = DummyOperator(task_id="compute_differences", dag=dag2)
update_dashboard = DummyOperator(task_id="update_dashboard", dag=dag2)
notify_new_data = DummyOperator(task_id="notify_new_data", dag=dag2)
compute_differences >> update_dashboard
```   
 
* 주의사항  
1) 'triggerDagRunOperator'를 통해 실행 시킨 DAG backfill 기능은 새롭게 dag를 실행 시키는 형태로 진행 됨  
<img width="542" alt="image" src="https://user-images.githubusercontent.com/65060314/175844885-c9cba58f-ca26-447b-9e50-aa8053dc5c63.png">  

## 5) 다른 DAG의 상태 값 폴링 하기
ExteranlTaskSensor 오퍼레이터의 서브기능의 통해 다른 DAG의 특정 task 상태 값을 가져올 수 있다  
```python
    ExternalTaskSensor(
        task_id="wait_for_etl_dag1",
        external_dag_id="figure_6_19_dag_1",
        external_task_id="etl",
        dag=dag4,
    )
```
* 주의 사항   
1) ExternalTaskSensor를 통해 확인하는 시점과 확인하고자하는 DAG의 실행 시간이 같아야만 확인이 가능함
  
<img width="524" alt="image" src="https://user-images.githubusercontent.com/65060314/175845944-826fc5c8-9337-4ef3-acf6-d2e2f6c33cc4.png">