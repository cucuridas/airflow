# 1. Airflow 소개

```
1) 파이썬 코드로 유연한 파이프라인 정리
2) 파이프라인 스케쥴링 및 실행
3) 모니터링과 실패 처리
4) 점진적 로딩 및 백필
5) Airflow가 적합하지 않은 경우
```

## 1) 파이썬 코드로 유연한 파이프라인 정리
------
Airflow는 파이썬 스크립트로 DAG의 구조를 설명하고 구성을 하게 된다. DAG 내부에서는 해당 DAG에서 필요로 하는 'default_argument'와 'task(operator)'에 대한 정의가 이루어지게 되고 시프트 연산자 표시를 통해 각 task가 어떠한 의존성을 가지게 되는지 정의하게 된다  
  
<img width="494" alt="image" src="https://user-images.githubusercontent.com/65060314/173225050-7958a1ae-ffb7-49a2-9685-addd505b00fc.png">a


## 2) 파이프라인 스케쥴링 및 실행 
------
Airflow는 파이프 라인을 언제 실행할 것인지 각각의 DAG에 대해 실행 주기를 정의 할 수 있는 정보를 명시하는데 이 정보는 'default_argument'에서 명시가 되며 각각의 task에도 따로 명시가 가능하여 세부적인 스케쥴링을 지원해주고 있다 

<img width="546" alt="image" src="https://user-images.githubusercontent.com/65060314/173225079-1a354922-cb37-4abf-8705-88ea41ddda00.png">

## 3) 모니터링과 실패 처리
------
Airflow-web-server를 통해 모니터링과 실패 처리에 대한 내용을 GUI형태로 진행 할 수 있다  
   
<img width="899" alt="image" src="https://user-images.githubusercontent.com/65060314/173225372-1ffe23d5-0ba9-45b9-b5ed-ab969dc7af3c.png">  

## 4) 점진적 로딩 및 백필
------
Airflow의 스케쥴 기능 중 장점으로 언급되는 부분은 DAG의 정의된 특정 시점에 트리거 할 수 있을 뿐만 아니라 최종시점과 예상되는 다음 스케줄 주기를 상세하게 알려 주는 것이다 이는 나중에 자세하게 알아보게 될 '빈도 기반의 스케쥴링'과 밀접한 연관이 있다라는 것만 알고 상세한 내용은 추후 설명하겠다

점진적 로딩은 task가 해당 빈도, 즉 주어진 시간슬롯에 대한 데이터만 처리를 하기 때문에 시간과 비용을 
아낄 수 있다

백필(backfill) 기능은 과거 시점에 시작한 데이터가 어떠한 이유에서 완료하지 못하였을 때 해당 시점의 데이터부터 다시 진행 할 수 있게끔 도와주는 기능이다  
  
<img width="1278" alt="image" src="https://user-images.githubusercontent.com/65060314/173225442-d7d962c8-fb9b-4974-ad65-539aa05c595d.png">

## 5) Airflow가 적합하지 않은 경우
------
* 스트리밍 워크플로 및 해당 파이프라인 처리 X
* 변경이 빈번한 동적 파이프라인 X
* 파이썬 프로그래밍 경험이 없는 팀
* 규모가 커짐에 따라 복잡 -> 엄격한 관리 필요


# 2. Airflow DAG 구조
```
1) 'DAG' 정의 코드 분석
2) 'Task' 와 'Operator'의 차이점
3) 스케쥴 간격으로 실행
4) 실패 태스크에 대한 처리 - 백필(backfill)
```

## 1) 'DAG' 정의 코드 분석
------
### 1-1) DAG 클래스 정의  

<img width="554" alt="image" src="https://user-images.githubusercontent.com/65060314/173227237-607532d8-bafc-439b-bcc4-da782aa3772c.png">

### 1-2) task 정의 

<img width="808" alt="image" src="https://user-images.githubusercontent.com/65060314/173227298-67eadf78-957b-4b96-aa21-d0a5972f0982.png">

## 2) 'Task' 와 'Operator'의 차이점
----
'Task' 와 'Operator' 모두 단일 작업을 수행한다는 공통점이 있고 두 용어를 같은 의미로서 사용한다,
하지만 개념적으로 볼때 'Task'는 올바른 실행을 보장하기 위한 'Operator'의 '래퍼(wrapper)'또는 'manager'로 생각해 볼 수 있다 

<img width="374" alt="image" src="https://user-images.githubusercontent.com/65060314/173227398-d0d352f0-cfc6-4722-b3ba-f5d95756ca56.png">

## 3) 스케쥴 간격으로 실행   
----
'schedule_interval' 인수 값을 통해 DAG 실행 빈도를 지정 할 수 있다  

<img width="509" alt="image" src="https://user-images.githubusercontent.com/65060314/173227538-3de6f58e-eef4-4bde-8ae9-8b34aef8482f.png">


## 4) 실패 태스크에 대한 처리 - 백필(backfill)
----
### 4-1) 특정 task 실패 발생
<img width="543" alt="image" src="https://user-images.githubusercontent.com/65060314/173227850-bc9bcaa9-2c5e-40b2-918a-09239568c12f.png">

### 4-2) 해당 task 클릭 후 오른 쪽 제어 창에서 'clear' 클릭  

<img width="680" alt="image" src="https://user-images.githubusercontent.com/65060314/173227982-63f186bc-df4e-42fd-85f3-1a666f16d1b3.png">
  
### 4-3) 실패 지점부터 다시 시작되는 모습  

<img width="357" alt="image" src="https://user-images.githubusercontent.com/65060314/173227999-a50bcd20-0604-4cd4-8ae1-94d083e54634.png">

# 3. Airflow에 스케쥴링 
```
1) '빈도 기반의 스케쥴링'과 '시점 기반 스케쥴링'
2) 실행 날짜를 사용하여 동적 시간 참조하기
3) 과거 시점의 작업 실행하기 - catchup 설정
4) task 디자인을 위한 모범 사례 - 원자성, 멱등성
```

## 1) '빈도 기반의 스케쥴링'과 '시점 기반 스케쥴링'
----
'시점 기반 스케쥴링'이란 특정 시점에만 해당 DAG를 실행 시키는 설정으로 서 리눅스 스케쥴링 'cron'과 동일한 형태로 설정을 하게 된다   
DAG 파이썬 코드 파일 내에서는 아래와 같이 정의 된다  
<img width="668" alt="image" src="https://user-images.githubusercontent.com/65060314/173229212-d43dab55-9a03-4321-b5cb-a77a9fc2379f.png">  

* cron 스케쥴 정의 형태   

<img width="416" alt="image" src="https://user-images.githubusercontent.com/65060314/173229024-f025c5c4-3a68-4a4b-a241-4de7b8c67976.png">  

'빈도 기반 스케쥴링' 특정 빈도에 맞춰 정의하는 스케쥴링을 의미하면 cron으로는 해당 식을 정의 할 수 없기 때문에 '빈도 기반 스케쥴링' 시에는 'timedelta' 라이브러리를 통해 정의 해주게 된다 

<img width="525" alt="image" src="https://user-images.githubusercontent.com/65060314/173229315-13314932-aab9-4294-9fc9-adeca40886cd.png">  

## 2) 실행 날짜를 사용하여 동적 시간 참조하기
----
Airflow 매개 변수 중 'execution_date'라는 매개변수는 스케줄 간격으로 실행 되는 시작 시간을 나타나는 타임스탬프이다 이는 DAG를 시작하는 시간의 특정 날짜가 아니라 그 날짜를 기준으로 실제로 처음 실행되는 시간을 의미하는 값이다

<img width="389" alt="image" src="https://user-images.githubusercontent.com/65060314/173229389-b34f402c-0aaf-4d8d-8b7a-69b37045eca8.png">

* 사용 방법 'jinja template' 을 통한 사용 방법 'context' kwarg를 사용한 사용방법  
    * jinja template 활용  
<img width="436" alt="image" src="https://user-images.githubusercontent.com/65060314/173229491-78ee64c4-a936-4212-bbc6-5f50db0a6260.png">    
    * 'context' 활용  
<img width="463" alt="image" src="https://user-images.githubusercontent.com/65060314/173229546-4ce36562-3ceb-4ef4-88d1-110e13418192.png">  

## 3) 과거 시점의 작업 실행하기 - catchup 설정
----
Airflow의 장점 중 하나인 백필 기능은 때때로 설정에 의해 다른 프로세스에 대한 병목현상을 일으키게 되는데 그 사례 중 하나가 catchup 설정으로 인한 병목 현상이다 catchup 설정이란 과거 시작 날짜를 지정하고 DAG가 활성화 하면 현재 시간 이전의 작업을 모두 완료후 진행하는 설정이다 이로 인해 과거 작업이 완료될 때까지 현재의 작업이 진행되지 못하는 병목현상을 일으키게 된다  

<img width="420" alt="image" src="https://user-images.githubusercontent.com/65060314/173229672-b8bb6d39-cda4-4200-be4e-4b2ca4f3a658.png">  

## 4) task 디자인을 위한 모범 사례 - 원자성, 멱등성
----
### 4-1) 원자성
원자성이란 데이터베이스 시스템에서 자주 사용되며 task가 실패 했을 경우 그 결과를 다른 task가 참조하지 않도록 하여 잘못된 결과가 발생하지 않도록 하는 것이다  

<img width="499" alt="image" src="https://user-images.githubusercontent.com/65060314/173229747-ef91951b-d32c-4951-b739-ac20f7f5e076.png">  

<img width="503" alt="image" src="https://user-images.githubusercontent.com/65060314/173229820-6b69df5a-e107-4c28-a418-05483b8c0989.png">  

### 4-2) 멱등성 
멱등성이란 어떠한 동일한 입력이 주어졌을 때 동일한 태스크를 여러번 호출해도 결과는 같아야 한다는 것이다 

<img width="537" alt="image" src="https://user-images.githubusercontent.com/65060314/173229881-a7c045ed-be3b-4419-ac07-88c28924e9e0.png">  

# 4. Airflow 콘텍스트를 사용하여 태스크 템플릿 작업하기

```
1) 오퍼레이터의 인수 템플릿 작업 - jinja template
2) context 변수 
3) python operator 템플릿
```

### 1) 오퍼레이터의 인수 템플릿 작업 - jinja template
앞에서 스케쥴링 시 jinja template을 활용한 정의 방법이 나왔었는데 jinja template이란 런타임시에 템플릿 문자열의 변수와 and 및 or 표현식을 대체하는 템플릿 엔진이다 템플릿 작성은 프로그래머로서 코드 작성 시점에는 값을 알기 어렵지만 런타임 시에 값을 할당하기 위해 사용한다  

<img width="436" alt="image" src="https://user-images.githubusercontent.com/65060314/173229491-78ee64c4-a936-4212-bbc6-5f50db0a6260.png">  

### 2) context 변수 
jinja tmeplate을 사용하는 거 외에도 DAG와 관련된 인수들이 정의되어 있는데 task가 실행될 때 context를 통해 해당 인수에 접근이 가능하다 context 변수에는 아래와 같다  

<img width="513" alt="image" src="https://user-images.githubusercontent.com/65060314/173231062-0a9754e9-b24f-4ac3-b5dc-2d7d8358d36b.png">  

### 3) python operator 템플릿
python operator를 통해 task를 생성할때 parameter 또는 생성되어 있는 인수를 참조하고자 할때 'kwargs'를 통해 context정보를 읽어와 사용하게 된다 'kwargs'는 dictionary형태의 데이터 타입을 가지고 있어서 get을 통해서도 파싱할 수 있고 배열의 메모리 접근법 (ex: test['a']['b'])로도 가능하다 또한 특정 context내의 특정 값을 가져오고자 할 떄는 context 변수 이름만 prameter값으로 넣어주면 해당 값을 가져와 내부로직을 진행하게 된다
* kwargs 를 통한 구성  
<img width="222" alt="image" src="https://user-images.githubusercontent.com/65060314/173231322-55bb7b1e-74fe-47d7-b428-cd3975979ca8.png">    
<img width="655" alt="image" src="https://user-images.githubusercontent.com/65060314/173231525-f3276511-624a-4f1e-ba49-8cb4b541dd58.png">
* context 내에 특정 값 가져오기  
<img width="462" alt="image" src="https://user-images.githubusercontent.com/65060314/173231490-3bb192d0-5d70-4875-8654-4e9ffe429209.png">
* parameter 값을 context 특정 값으로 받기  
<img width="555" alt="image" src="https://user-images.githubusercontent.com/65060314/173231460-0b6e8306-5635-45ff-8dde-59a05d8285ea.png">

# 5. 태스크간 의존성 정의하기
```
1) 선형 의존성 유형
2) 팬인/팬아웃 의존성
3) 브랜치 하기
4) 트리거 규칙에 대한 추가 정보
5) 태스크 간 데이터 공유 - xcom
```

## 1) 선형 의존성 유형
-------
'선형 의존성'이란 이전의 태스크의 결과값이 다음 태스그의 인풋값으로 사용될 때 '선형 의존성'을 가진다라고 한다 DAG에서 의존성을 명시할 때 비트 시프트 연산자를 통해 두 태스크 간의 '선형 의존성'관계를 나타낼 수 있다  

<img width="312" alt="image" src="https://user-images.githubusercontent.com/65060314/173232664-c62ff0e5-84c1-4ada-9e75-da0b9e3a9894.png">

## 2) 팬인/팬아웃 의존성
-------
팬인/팬아웃 이란 태스크간의 복잡한 의존성을 의미한다 예시로 두개의 task A 와 B가 병렬로서 처리가 되고 완료 된 후 task C라는 작업으로 가는 DAG가 있을 때 해당 TASK A,TASK B와 task C 는  '팬인' 된 의존성 task 형태라고 할 수 있다 (그 반대는 '팬 아웃')

<img width="340" alt="image" src="https://user-images.githubusercontent.com/65060314/173232810-5a64d580-7ee3-4f50-b76c-55ff49ece0ad.png">

<img width="462" alt="image" src="https://user-images.githubusercontent.com/65060314/173232887-24d0eab4-008a-4b39-b9fb-3d7821bdacbd.png">

## 3) 브랜치 하기
-------
### 3-1) task 내에서 브랜치 하기
task 내에서 사용하는 'python_callable'인수의 호출되는 함수 값에서 특정 조건에 따라 분기를 나누는 방식이다   
<img width="387" alt="image" src="https://user-images.githubusercontent.com/65060314/173232998-b71ab84a-2732-413d-bcb0-3b93215154de.png">
  
<img width="595" alt="image" src="https://user-images.githubusercontent.com/65060314/173233028-b132b696-c1a2-4501-88db-4fc1f30b2af9.png">

### 3-2) DAG 내부에서 브랜치 하기 - branch operator
DAG를 작성하게 될 떄 Airflow 에서 제공하는 branch operator를 통해 분기를 나누는 방법이다 기본 베이스 형태는 python operator 와 동일하다   

![image](https://user-images.githubusercontent.com/65060314/173233143-159111dd-0b4e-45a6-825b-3b50ebfcd5de.png)
  
![image](https://user-images.githubusercontent.com/65060314/173233178-2d1b067a-3035-407e-bc95-59e37cb30642.png)
  
## 4) 트리거 규칙에 대한 추가 정보
-----
트리거 규칙이란 task의 의존성 기능과 같이 Airflow의 task 가 실행 준비가 되어 있는지 여부를 결정하고 그 결정에 맞춰 다음 task 실행 할 것인지에 대한 설정이다 기본 트리거 규칙은 'all _sccess'로 되어 있으며 이 설정은 앞의 up_stream task 작업이 모두 성공으로 끝나야만 down_stream task를 실행 시키겠다는 설정이다  
  
<img width="505" alt="image" src="https://user-images.githubusercontent.com/65060314/173233446-8e350641-5d93-4749-9c42-7466d6e3f7ce.png">


* 트리거 규칙의 value 값

| 트리거 규칙 | 동작 | 사용 사례 |
| -------- | -------- | -------- |
| all_success | 모든 상위 태스크가 성공적으로 완료되면 트리거 | 기본 트리거 규칙 |
| all_failed | 모든 상위 태스크가 실패했거나 상위 태스크의 오류로인해 실패했을 경우 | 오류 처리 코드를 트리거 하기위해 사용 |
| all_done | 결과 상태에 상관없이 앞선 작업이 완료 되었을 때 | 모든 태스크가 완료 되었을 때 실행할 청소 코드 실행 |
| one_failed | 하나 이상의 상위 태스크가 실패 했을 경우 트리거(다른 상위 타스크의 완료를 기다리지 않음) | 알림 또는 롤백과 같은 일부 오류 처리에 사용 |
| one_success | 한 부모가 성공하자마자 트리거 됨(다른 상위 타스크의 완료를 기다리지 않음) | 하나의 결과를 사용할 수 있게 되는 즉시 다운스트림 연산/알림 트리거 |
| none_failed | 실패한 상위 태스크가 없지만 태스크가 성공 또는 건너뛴 경우 트리거 | 브랜치 오퍼레이터 사용시 사용 |
| none_skipped | 건너뛴 상위 태스크가 없지만 태스크가 성공 실패 한 경우 트리거 | 모든 업스트림 태스크가 실행된 경우 해당 결과를 무시하고 트리거 |


## 5) 태스크 간 데이터 공유 - xcom
----
xcom이란 task 끼리의 데이터를 공유하고자 할 때 사용하는 Airflow 기능 중 하나 이다 'xcom_push(key='key_value',value='value_value')' 형태로 데이터를 넣게 되고 'xcom_pull(key='key_value')'를 통해 push된 데이터를 사용하게 된다  

![image](https://user-images.githubusercontent.com/65060314/173233996-d9978f04-53e3-4970-afa7-2cf1ec4d1bd3.png)

<img width="675" alt="image" src="https://user-images.githubusercontent.com/65060314/173234022-ef222b3a-b058-4287-ba85-9c3c91cc0281.png">  

* xcom 사용시 고려사항  
    1. 묵시적인 의존성이 필요
    2. 원자성을 무너뜨리는 패턴이 될 가능성이 있음
    3. 직렬화를 지원해야한다는 기술적 한계  
        database 별 제한사항  
        * SQLite - BLOB 유형으로 저장 2GB
        * PostgreSQL - BYTEA 유형으로 저장, 1GB 제한
        * MySQL - BLOB 유형으로 저장, 64KB 제한
        