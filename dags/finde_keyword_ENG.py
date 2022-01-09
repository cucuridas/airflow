from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
import nltk
from module.module_redis import dags_redis
from module.module_extraction import Keyword_extraction


#redis의 tag를 기준으로 데이터를 가져와야함
defluat_param  = {"result_data" : "NLTK is a leading platform for building Python programs to work with human language data. python python programs human hu to with platform"}


dag = DAG(
        dag_id='Finde_keyword_WF_ENG',
        description='Finde keyword workflow',
        schedule_interval='0 12 * * *',
        start_date=datetime(2017, 3, 20), catchup=False,
        params = defluat_param,
        tags=["keyword"]
        )



#모든 input 값은 Json 형태로 들어옴으로 '**'표시를 통해 input값 처리
def Finde_keyworkd(**kwargs):

        print(kwargs['params'].get('result_data'))

        #nltk를 통한 단어 추출 - 해당내용에 추출되지 못한 단어가 존재할 경우 Konlp의 사전에 추가해주어야함
        words = nltk.word_tokenize(kwargs['params'].get('result_data'))
        
        #추출된 keywords들의 빈도수를 포함한 Dic
        keywords = {}
        
        #추출된 단어를 토대로 빈도수를 측정
        for word in words :
                try: keywords[word] += 1
                except: keywords[word] = 1

        #Keywords에서 가장 많이 언급된 Key 값을 추출-> 함수명 keyword_extraction       
        
        return_dic = {'keyword':Keyword_extraction(keywords),'Text_data':kwargs['params'].get('result_data')}

        #module_redis에서 redis 클래스를 통해 저장 
        r=dags_redis()

        r.redis_set("ex_data",return_dic)
        #value = r.redis_get("ex_data")
        
       
        return 




exec_extract = PythonOperator(
        task_id = 'Finde_keyword_ENG',
        python_callable = Finde_keyworkd,
        provide_context=True,
        dag = dag
        )
