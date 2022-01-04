from datetime import datetime
from airflow import DAG
from airflow.operators.python import PythonOperator
from konlpy.tag import Kkma
from konlpy.utils import pprint



dag = DAG('Finde_keyword_WF', description='Finde keyword workflow',
          schedule_interval='0 12 * * *',
          start_date=datetime(2017, 3, 20), catchup=False)




def Finde_keyworkd(**kwargs):
        Kkma1 = Kkma()
        words = Kkma1.nouns(kwargs['params'].get('result_data'))
        setnece = Kkma1.sentences(kwargs['params'].get('result_data'))

        print(words)
        print(sentences)





exec_extract = PythonOperator(
        task_id = 'Finde_keyworkd',
        python_callable = Finde_keyworkd,
        provide_context=True,
        dag = dag
        )
