import redis
from urllib.parse import urlparse
import socket
import json

def connect_():
    #
    # 레디스 연결
    try:
        rd = redis.StrictRedis(host='15.165.124.23', port=58542, db=0)
        print('연결 성공')
    except:
        print('연결 실패....')
    return rd

def redis_set(rd,key,jsonData):
    jsonDataDict = json.dumps(jsonData, ensure_ascii=False).encode('utf-8')
    rd.set(key,jsonDataDict)
    return "인 메모리 저장 완료"
    

def redis_get(rd,key):
    value = rd.get(key)
    return value