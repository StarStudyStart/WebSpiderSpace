#coding:utf-8
from redis import StrictRedis, ConnectionPool
'''键值类型数据库'''

#连接数据库
#redis = StrictRedis(host='localhost', port=6379, db=0) 
url='redis://@localhost:6379/0'
#pool = ConnectionPool.from_url(url)
pool = ConnectionPool(host='localhost', port=6379, db=0)
redis = StrictRedis(connection_pool=pool)
#数据操作
#redis.set('sexy','male')
print(redis.get('sexy'))
print(redis.get('name'))