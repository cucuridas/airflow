# -*- coding:utf-8 -*-
from datetime import datetime
from logging import Logger, log
from airflow import DAG
from airflow.operators.python import PythonOperator
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from module.module_redis import dags_redis
import json


defluat_param = {"url": "https://www.naver.com","selector_position":"body"} 

dag = DAG(
        dag_id = 'crolling_TEXT_WF', 
        description='Crolling_WF for text data',
        schedule_interval='0 12 * * *',
        start_date=datetime(2017, 3, 20), catchup=False,
        params=defluat_param,
        tags=["parseData"]
        )


def crollingText(**kwargs):
    #예제 json {"url": "https://www.naver.com","selector_position":"body"}    
    op = webdriver.ChromeOptions()
    op.add_argument("headless")
    op.add_argument("no-sandbox")
    op.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('/workspace/Photopolio_/chromedriver',chrome_options=op)
    print(kwargs['params'].get('url'))
    driver.get(kwargs['params'].get('url'))



    sel_Page_Name = driver.find_element_by_css_selector(kwargs['params'].get('selector_position'))

    #print(sel_Page_Name.text)
    
    return_data = sel_Page_Name.text

   
    dags_redis().redis_set("pashingData",return_data)    

    driver.quit()


    
    return return_data


exec_extract = PythonOperator(
        task_id = 'CrollingText',
        python_callable = crollingText,
        provide_context=True,
        dag = dag
        )


