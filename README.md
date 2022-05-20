# Apache-Airflow 학습을 위한 개발 환경 구성

## docker-compose 를 활용하여 구성

<span style='background-color: #ffdce0'> \* docker-compose로 구성하기에 앞서 docker 와 관련된 패키지들이 설치되어있어야합니다 </span>

다운 받고자 하는 디렉토리에서 해당 명령어로 docker-compose 파일 다운로드


```python
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/2.3.0/docker-compose.yaml'
```

명령어를 통해 container 생성


```python
docker-compose up
```

## container 내부에서 DAG 개발 진행 방법

* Remote - Containers 확장 패키지를 VS code 에 설치

![image](https://user-images.githubusercontent.com/65060314/169421538-5c38e88b-efd6-4f56-aa9f-22a40aad8068.png)

* ‘ctl + shift + p’ 를 클릭 후 Remote - Containers 실행

![image](https://user-images.githubusercontent.com/65060314/169421706-8eb3fac9-25c2-4681-a367-d1d2001a285e.png)

* 출력 되는 Continer 목록 중 'tg-chatbot_airflow-webserver_1' 클릭하여 접속

![image](https://user-images.githubusercontent.com/65060314/169421820-9c8352d3-9a69-4dad-b62f-7b737d734ab1.png)


* ‘폴더열기’ 버튼을 통해 '/opt/airflow/dags' 디렉토리로 이동

![image](https://user-images.githubusercontent.com/65060314/169421857-048b658b-9e23-459e-8baa-8189185a00c7.png)

* 최초 설치 시 container와 vscode간 사용할 python 확장패키지 설치 필요

![image](https://user-images.githubusercontent.com/65060314/169421915-ae1b716c-4b1e-4317-9c6b-f41a845ee1db.png)

* 'ctl + shift + p' 를 클릭 후 'python select interpreter'를 통해 python version을 Container 내부의 python version으로 변경 ('python 3.7.13')

![image](https://user-images.githubusercontent.com/65060314/169421981-8ec5cb68-f147-4f57-aeb2-d44ad20fd94b.png)

![image](https://user-images.githubusercontent.com/65060314/169422023-3da4039e-7000-438d-a892-8bca7d0f1d18.png)

* 모듈이 정상적으로 import 되는 모습, 정의로 이동시 정상작동되는 모습

![image](https://user-images.githubusercontent.com/65060314/169422135-b323572e-c2a4-4d9a-b194-af4c60ae13bc.png)

![image](https://user-images.githubusercontent.com/65060314/169422168-c192ef8a-645f-4c07-91d9-d153447569f8.png)


```python

```
