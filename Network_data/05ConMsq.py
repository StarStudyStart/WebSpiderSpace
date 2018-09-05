import pymysql
conn = pymysql.connect(host = '127.0.0.1',user='root',passwd='admin',db='mysql')
cur = conn.cursor()
cur.execute("USE scraping")
cur.execute('INSERT INTO pages(title,content) VALUES ("Geany","The geany is an IDE")')
cur.connection.commit()

cur.execute("SELECT * FROM pages")
print(cur.fetchone()) # 读取cur2最近一次执行查询操作的结果，fetch one 返回单行
cur.close()
conn.close()
