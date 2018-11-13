#coding:utf-8
import pymongo

#创建连接对象
#client = MongoClient(host='localhost', port=27017)
client = pymongo.MongoClient(host='localhost')

#指定数据库
db = client.test

#指定集合
collection = db.students

'''操作数据'''
#删   清除原有数据
collection.delete_many({'age':{'$gt':18}})

#增
student1 = {
    'id':'12035077',
    'name':'Bob',
    'age':24,
    'gender':'male'
}
student2 ={
    'id':'12035079',
    'name':'Mike',
    'age':26,
    'gender':'male'
}
#result = collection.insert_one(student1)
#print(result)
results = collection.insert_many([student1, student2])
print(results)
print(results.inserted_ids)
print('=============================================')

#查
result = collection.find_one({'name':'Mike'})
print('=============================================')
print(result)
results = collection.find({'age':{'$gt':20}})
for result in results:
    print(result)
print('=============================================')

#改
condition = {'name':'Mike'}
student = collection.find_one(condition)
student['age'] = 19
result = collection.update(condition, {'$set': student})
print(result)
result = collection.find_one({'age':19})
print(result)
