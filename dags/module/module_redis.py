import redis

# 레디스 연결
rd = redis.StrictRedis(host='13.209.89.224', port=53635, db=0)

#rd.set("[키]", "[값]")

print(rd.get("[키]").decode('utf-8'))