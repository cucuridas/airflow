import redis
import json

class dags_redis:
        #객체 생성과 함께 Connection정보를 반환
        def __init__(self):
                try:
                        self.con = redis.StrictRedis(host='15.165.124.23', port=58542, db=0)
                        print('연결 성공')
                except:
                        print('연결 실패....')
       
        #Json 형태로 변환하여 해당 데이터를 DB에 저장하게 됨
        #key : Key로 사용하게 될 String parameter -> tag 값으로 연관되어 있는정보를 가져오는걸로 
        #jsonData : json Data로 변화하게 될 데이터 (Dic type으로....)
        def redis_set(self,key,jsonData):
                jsonDataDict = json.dumps(jsonData, ensure_ascii=False).encode('utf-8')
                self.con.sadd(key,jsonDataDict)
                return print("redis 서버 메모리 저장 완료")
        
        
        #해당 태그에 몇개의 데이터가 있는지 조회
        def redis_C_get(self,key):
                value = self.con.scard(name=key)
                return value
                
        #해당 태그의 데이터 조회
        def redis_D_get(self,key):
                value = self.con.smembers(key)
                return value
        