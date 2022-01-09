from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from konlpy.tag import Okt
from konlpy.utils import pprint
from module.module_redis import dags_redis

defluat_param  = {"result_data":" 외국인 고령자와 외국인 장애인에게 복지수당을 지급합니다.외국인이 두 번 반복이 되므로.. 생략하고자 할 때..외국인 , 장애인에게 복지수당을 지급합니다.라고 할 경우, 외국인 고령자/ 장애인으로 생각하여, 장애인은 외국인이 아니라고 판단할 수 있을 거 같아서요.이러할 경우... 어떤 문장부호를 쓴다면.. 고령자와 장 고령자, 고령자 고령"}
redis_param = {"result_data":dags_redis().redis_get("pashingData")}

dag = DAG(
        dag_id='Finde_keyword_WF',
        description='Finde keyword workflow',
        schedule_interval='0 12 * * *',
        start_date=datetime(2017, 3, 20), catchup=False,
        params = redis_param,
        tags=["keyword"]
        )



#모든 input 값은 Json 형태로 들어옴으로 '**'표시를 통해 input값 처리
def Finde_keyworkd(**kwargs):

        print(kwargs['params'].get('result_data'))

        #okt를 통한 단어 추출 - 해당내용에 추출되지 못한 단어가 존재할 경우 Konlp의 Dic을 추가해주어야함
        okt1 = Okt()
        words = okt1.nouns(kwargs['params'].get('result_data'))
        
        #추출된 keywords들의 빈도수를 포함한 Dic
        keywords = {}
        
        #추출된 단어를 토대로 빈도수를 측정
        for word in words :
                try: keywords[word] += 1
                except: keywords[word] = 1


        #Keywords에서 가장 많이 언급된 Key 값을 추출       
        from module.module_extraction import Keyword_extraction

        return_dic = {'keyword':Keyword_extraction(keywords),'Text_data':kwargs['params'].get('result_data')}


        #module_redis에서 redis 클래스를 통해 저장 
        r=dags_redis()

        r.redis_set("ex_data",return_dic)
        
        return return_dic




exec_extract = PythonOperator(
        task_id = 'Finde_keyworkd',
        python_callable = Finde_keyworkd,
        provide_context=True,
        dag = dag
        )
