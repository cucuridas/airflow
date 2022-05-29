# Ariflow
회사 내부에서 cloud service를 진행 하기위해 'Airflow' 도입하게 되었다. 나중에 기본 개념 및 concept을 설명할 때에 이야기하겠지만 'Airflow'는 pipline 관리 및 구성에 편리하도록 제작된 툴이니만큼 사실 streaming(실시간) service에는 용이하지 못한 부분이 있을 것으로 도입시기 때 부터 언급되었다. 현재는 task를 통한 pipline 구축에 대한 이점을 더 높게 보고 진행하기로 정해진 시점이니 해당 내용에대해 공부를 진행하고 앞선 말한 과제?(실시간 서비스)부분을 어떻게 보완할 것인지 고려해보도록 하겠다


## Airflow 란?
### 개요
![image](https://user-images.githubusercontent.com/65060314/170859360-1481a379-2cb7-47d3-a8a3-673da5ec8064.png)
(공식 document 페이지 이미지)
![image](https://user-images.githubusercontent.com/65060314/170861123-5fc833c3-2f4d-4fd0-a88e-3da111cf339b.png)
(webserver까지 정상적으로 올려지면 요런식의 페이지에 접속가능)

Airflow 공식 홈페이지의 documnet를 들어가게되면 Airflow 대한 여러가지 concept이나 장점에 대해 이야기해주는데 한줄로 요약하면 아래와 같다

"Airflow is a platform to programmatically author, schedule and monitor workflows."
(에어플로우는 프로그래밍 방식으로 워크플로우를 작성, 예약 및 모니터링하는 플랫폼입니다.)

정말 저 한줄로 설명한게 가장 Airflow가 무엇인가? 에 대한 내용을 모두 담고 있는거 같다 기본 언어로서 'python'을 사용하여 'DAG'와 'DAG' 내부에서 'task'를 구현함으로써 워크플로우를 작성하고 해당 DAG를 DB에 저장하여 스케쥴링을 통한 작업을 진행하는 pipline 형태의 software라고 보면 된다 

### 장점
'Airflow' 홈페이지에서는 4가지 장점을 보여주고있는데 각각의 원칙에 대해서 설명을 하자면  
Dynamic: python 코드로 작성 된 코드를 통해 동적 파이프라인 생성을 가능하게 한다. 내부적으로 모듈을 제공하여 instance를 생성하고 해당 규격에 맞춘 파이프라인을 작성할 수 있도록 제공한다  
Extensible: 또한 여러기능 (2.3.0 버전부터 decorater 기능 등)을 통한 모듈 확장 방식을 도입하여 확장함에 있어서 자유롭다 
Elegant: jinja template 을 통해 작성한 script를 Airflow core에 파라미터화 할 수 있다  
Scalable: Airflow는 모듈식 아키텍처를 가지고 있으며 메세지 큐를 통한 작업의 조율을 진행 할 수 있다. 

* Airflow는 data streamin solution이 아니기에 task의 데이터의 이동에 대해 관리를 할 수 없다


## DAG란?
기본 개념으로는 방향성 비순환 그래프 (Directed Acyclic Graph)라는 개념을 바탕으로 제작되어진 알고리즘이다, 방향성은 가지지만 순환은 하지않는 그래프를 의미한다 
'Airflow'에서의 DAG는 위와같은 개념을 바탕으로 제작되어진 하나의 pipline이라고 보면 된다
내부에서는 DAG 하위 개념이 'task'가 정의되게 되는데 operator 클래스를 통한 instance 생성 정보로 해당 task의 내용이 채워지게 된다

![image](https://user-images.githubusercontent.com/65060314/170860430-c891f9e6-b79b-4b19-8c33-a520151c6240.png)


## Airflow 기본 동작 방식 - concept

각 노드들의 역할을 aws 공식 홈페이지에서 확인 할 수 있었는데 

```python
Scheduler: scheduler는 DAG 및 task를 모니터링하고 종속성이 충족된 task instance를 트리거하는 지속적인 서비스입니다. scheduler는 Airflow의 configuration에 정의된 executor를 호출하게 됩니다.
Executor: executor는 task instance를 실행하는 방법을 제공합니다. Airflow는 기본적으로 다른 유형의 executor를 제공하며 Kubernetes executor와 같은 custom executor을 정의할 수 있습니다.
Broker: broker는 메시지를 대기열에 넣고(task가 실행되도록 요청) executor와 worker 간의 커뮤니케이터의 역할을 합니다.
Worker: task가 실행되고 task의 결과를 반환하는 실제 노드입니다.
Web Server: Airflow UI를 렌더링하는 웹 서버입니다.
Configuration file: 사용할 executor의 설정, Airflow의 Metadata database 연결, DAG 및 저장소 위치와 같은 설정을 구성합니다. 동시 실행 및 병렬 처리 제한 등을 정의 할 수도 있습니다.
Metadata Database: DAGS, DAG의 실행, task, 변수 및 연결과 관련된 모든 메타데이터를 저장하는 데이터베이스입니다.
```

![image](https://user-images.githubusercontent.com/65060314/170861167-0cc7ce00-71e8-46e9-a773-824eba482ee3.png)
(이미지 출처: https://aws.amazon.com/ko/blogs/korea/build-end-to-end-machine-learning-workflows-with-amazon-sagemaker-and-apache-airflow/)

실제로 작업이 이루어지는 task는 아래와 같다( 자료를 찾아서 확인해 보았을때는 현재와 같은 프로세스이나 2.2.0 version 이후 변화가 있는듯 하여 확인중)

1. enginer가 DAG를 작성
2. scheduler가 해당내용을 metadata(database)에 source코드 등을 저장
3. scheduler가 예약된 작업을 excutor에게 전달 
4. excuter가 정의되어진 task(operator)의 내용을 파악하여 worker에게 전달





```python

```
