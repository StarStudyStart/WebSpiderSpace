# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
import pymysql

from scrapy import Request
from scrapy.exceptions import DropItem
from scrapy.pipelines.images import ImagesPipeline

class MongoDBPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
     
    @classmethod
    def from_crawler(cls, crawler):
        #实例化自身，并且传入全局参数
        return cls(
            mongo_uri = crawler.settings.get('MONGO_URI'),
            mongo_db = crawler.settings.get('MONGO_DB')
        )
        
    def process_item(self, item, spider):
        #处理返回数据，存储到MONGOdb的制定集合中
        self.db[item.collection].insert_one(dict(item))
        return item
        
    
    def open_spider(self, spider):
        #初始化数据库
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        
    def close_spider(self, spider):
        #关闭数据库
        self.client.close()        
        
class MySQLPipeLine(object):
    '''创建数据库： CREATE DATABASE images360 DEFAULT CHARACTER SET utf-8 COLLATE utf8_general_ci
        创建数据表 CREATE TABLE images (id VARCHAR(255) PRIMARY KEY,
                    url VARCHAR(255) NULL, title VARCHAR(255),
                    thumb VARCHAR(255) NULL)
    '''
    
    def __init__(self, database, host, user, pwd, port, create_db,create_tb):
        
        self.database = database
        self.host = host
        self.user = user
        self.pwd = pwd
        self.port = port
        self.create_db = create_db
        self.create_tb = create_tb
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            database = crawler.settings.get('MYSQL_DATABASE'),
            host = crawler.settings.get('MYSQL_HOST'),
            user = crawler.settings.get('MYSQL_USER'),
            pwd = crawler.settings.get('MYSQL_PWD'),
            port = crawler.settings.get('MYSQL_PORT'),
            create_db = crawler.settings.get('MYSQL_CREATE_DB'),
            create_tb = crawler.settings.get('MYSQL_CREATE_TB'),
        )
        
    def process_item(self, item, spider):
        #构造动态的sql语句，并且动态执行
        data = dict(item)
        keys = ', '.join(data.keys())
        values = ', '.join(['%s']*len(data))
        sql = 'insert into %s (%s) values (%s)' % (item.table, keys, values)
        self.cursor.execute(sql, tuple(data.values()))
        self.db.commit()
        return item
                
    def open_spider(self, spider):
        #spider创建时进行数据库链接，获取游标等初始化操作
        self.db = pymysql.connect(self.host, self.user, self.pwd, self.database,
            charset='utf8', port=self.port)
        self.cursor = self.db.cursor()
        '''
        #如果images数据库存在则不创建，不存在则创建
        self.cursor.execute(self.create_db)
        #创建数据库后需重新连接
        #如果images360表存在则不创建，不存在则创建
        self.cursor.execute(self.create_tb)
        '''
        
    def close_spider(self, spider):
        #spider 关闭时断开数据库连接
        self.db.close()
        
        
class ImagePipeline(ImagesPipeline):
    ''' 提取返回的图片链接
        放入队列然后下载到本地
    '''
    
    def get_media_requests(self, item, info):
        #提取item中的链接放入队列中
        yield Request(item['url'])    
    
    def file_path(self, request, response=None, info=None):
        #返回要保存的文件名
        url = request.url
        file_name = url.split('/')[-1]
        return file_name
    
    def item_completed(self, results, item ,info):
        #剔除下载失败的item 不将该item存放入数据库中
        image_paths = [x['path'] for ok, x in results if ok ]
        if not image_paths:
            raise FropItem('Image Downloaded Faield')
        return item
