# 동시성과 병렬성이란?
동시성이란 물리학에서 서로 다른 형태의 사건이 동시에 일어나는 현상을 말하는데 컴퓨터에서는 해당내용에 대한 정의를 '동시에 실행되는 것 같이 보이는 것'이라고 명시 되어 있다, 병렬성의 경우 실제로 멀티코어에서 멀티쓰레드를 동작시킴으로써 '보여주는 것'이 아닌 '여러작업이 동시에 처리 되는것'으로 정의되고 있다 

![image](https://user-images.githubusercontent.com/65060314/170863412-6533260c-5391-428a-bae3-8adce9cba8d9.png)
(출처:https://seamless.tistory.com/42)

위의 그림과 같이 동시성은 하나의 코어에서 논리적으로 해당 task를 동시에 같이 실행 하게끔 진행 하는 반면에 병렬성은 하나의 코어가 아닌 여러개의 코어를 활용해 물리적으로 동시에 실행하는 개념이다

# 2. Airflow worker 의 cpu 리소스 제한
Airflow에서 제공되는 기본 docker image를 활용하여 환경을 구성하게되면 사용할 수 있는 동시 task에 대한 부분이 상당히 제한적이다, 또한 On premise 환경으로 구축되어 진 Airflow의 경우 CPU resource에 대한 자원이 제한적임으로 task에 대해 자원의 접근을 제한할 필요성이 생기게된다 이때 사용하게 되는 option이 pool이며 이 pool은 Airflow를 구성하고 있는 celery engin을 통한 동시처리 개념이다
## 2-1 pool 이란?
앞서 말한것과 같이 pool의 개념은 celery를 통해서 정의가 되는데 celery란 무엇인지 간단하게 설명을 하자면  
1. 비동기 작업 큐(실시간 처리에 중점을 둠)
2. 동기/비동기 처리가능
3. 작업단위 task, 작업자는 worker
4. 메세지 브로커를 활용하여 진행

으로 설명 할 수 있다
airflow excutor가 작업을 celery의 worker로 전달해 주고 위의 기능을 통해 작업을 진행 하는 프로세스이다 이때 동시성에 대한 부분을 DAG-task를 정의 할때 명시 할 수 있는데 이 옵션을 통해 celery worker가 cpu resource 사용하는 것에 대한 제한 할 수 있다

![image](https://user-images.githubusercontent.com/65060314/170863893-e3ce7afc-1803-4afd-a6c1-82368566c390.png)

pool 설정을 하는 방법에는 아래와 같다  

1. Airflow-web-ui 에서 Admin의 pools를 클릭한다  

![image](https://user-images.githubusercontent.com/65060314/170863990-0e385b52-e5c9-48a1-8ef3-4dce0ec6139b.png)

2. '+' (Add a new record)를 통해 새로운 pool을 생성한다  

<img width="546" alt="image" src="https://user-images.githubusercontent.com/65060314/170864122-a196d082-dbd9-432b-964d-c11b864e695e.png">

3. 'DAG' 내부 task에서 해당 argument의 값을 새로 생성한 pool로 채워준다 

```python
    process_c = BashOperator(
        owner="choi",
        task_id="process_c",
        retries=3,
        retry_delay=datetime.timedelta(seconds=10),
        bash_command="echo '{{ti.try_number}}' && sleep 8",
        #해당 내용으로 명시
        pool="test_pool"      

    )
```
* 작업이 진행 중일때 같은 level에 있는 task임에도 순서대로 진행 되는 모습

![concurrency_limit2](https://user-images.githubusercontent.com/65060314/170871684-cba36085-8700-4d76-9872-cabb9bf02c54.gif)

## 2-2 priority_weight을 통한 pool 내부에서의 우선순위 정의

2-1 에서 pool을 통해 같은 level의 작업이 동시적으로 실행 되었을 때 사용하는 cpu resource를 제한 하였다면 priority_weight 옵션은 같은 level의 task가 순차적으로 실행 될때 우선순위(중요도 값)을 지정하는 옵션이다
따라서 priority_weight과 pool은 밀접한 관계를 가지게 되는데 

만약 한개의 쓰레드를 활용하는 pool에서 3개의 task가 동시에 실행 된다고 가정을 하자. 1번 task는 db read, 2번 task는 db update, 3번 task는 db delete가 존재하게 되는데 이때 raice condition이 일어나지 않게 하기 위해  선행되야하는 작업이 있을 것이다 지금 같은 task의 경우 delete의 작업이 가장 우선적으로 진행 되어야하면 후에 update read의 경우 소프트웨어 개발 요건에 맞춰 중요도를 매핑하게 될 것 이다  이때 사용하는 옵션이 priority_weight이다

![image](https://user-images.githubusercontent.com/65060314/170864695-9b85248d-47ba-4ee7-8f57-bcc86473f4fd.png)

* DAG에서 task 옵션 설정 내용  

```python
process_a = BashOperator(
        owner="choi",
        task_id="process_a",
        retries=3,
        retry_delay=datetime.timedelta(seconds=10),
        bash_command="echo '{{ti.try_number}}' && sleep 8",
        pool="test_pool",
        priority_weight = 7

    )

    process_b = BashOperator(
        owner="choi",
        task_id="process_b",
        retries=3,
        retry_delay=datetime.timedelta(seconds=10),
        bash_command="echo '{{ti.try_number}}' && sleep 8",
        pool="test_pool",
        priority_weight = 6       

    )

    process_c = BashOperator(
        owner="choi",
        task_id="process_c",
        retries=3,
        retry_delay=datetime.timedelta(seconds=10),
        bash_command="echo '{{ti.try_number}}' && sleep 8",
        pool="test_pool",
        priority_weight = 8        

    )
```

* Airflow web ui 에서 확인되는 모습  
![concurrency_limit](https://user-images.githubusercontent.com/65060314/170871418-160c3fd7-c995-42a1-b77a-f89ea5ace93f.gif)

* "cross_downstream"이라는 모듈을 통해 연관 downstream 설정을 하여 동시 task process를 명시 할 수 있음

# 3. 동적인 resource 분배를 통한 한계점 극복

해당 내용은 추후 kubernetes operator를 통한 scale통해 확인하도록 할 예정
