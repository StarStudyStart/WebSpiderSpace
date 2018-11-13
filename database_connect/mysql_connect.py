import pymysql

#创建数据库
db = pymysql.connect(host='localhost',user='root', password='admin', port=3306)
#获取游标对象
cursor = db.cursor()
cursor.execute('SELECT VERSION()')
data = cursor.fetchone()
print('Database version:', data)
cursor.execute("CREATE DATABASE IF NOT EXISTS spiders DEFAULT CHARSET UTF8MB4;")
print('Database version:', data)
db.close()

#链接已经创建的数据库，新建表
db = pymysql.connect(host="localhost", user='root', password='admin', db='spiders')
cursor = db.cursor()
sql = 'CREATE TABLE IF NOT EXISTS students(id VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, age INT NOT NULL, PRIMARY KEY(id))'
cursor.execute(sql)
db.close

#增
table = 'students'
data ={
    'id':'12035078',
    'name':'StarLi',
    'age': 25,
}
keys = ', '.join(data.keys())
values = ', '.join(['%s']*len(data))

db = pymysql.connect(host='localhost', user='root', password='admin',
    db='spiders')
cursor = db.cursor()

#sql = 'INSERT INTO students(id, name, age) VALUES (%s, %s, %s)'
sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE '.format(table=table, keys=keys, values=values)
#ON DUPLICATE KEY UPDATE主键重复则更新数据，不重复则插入
update = ','.join(['{key} = %s'.format(key=key) for key in data])
sql +=update
print(sql)

try:
    cursor.execute(sql, tuple(data.values())*2)
    print('Successful')
    db.commit() #数据库的commit方法 db.commit()
except:
    print('Failed!')
    db.rollback()
    
#改
sql = 'UPDATE students SET age = %s WHERE name = %s'
try:
    #cursor.execute(sql, (26, 'Mike')) # name ='Mike' 'Mike'为字符串，不能写成参数Mike
    #db.commit()
    print('Successful')
except:
    print('Failed!')
    db.rollback()
    
#删
table = 'students'
condition = 'age > 20'
sql = 'DELETE FROM {table} WHERE {condition}'.format(table=table,
    condition =condition)
try:
    #cursor.execute(sql)
    #db.commit()
    print('Successful!')
except:
    print('Failed')
    db.rollback()
    
#查
sql = 'SELECT * FROM students WHERE age>20'
cursor.execute(sql)
row= cursor.fetchone()
'''while row:
    print('Row:'+row)
    row =cursor.fetchone()
    '''
db.close()