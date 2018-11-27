#coding:utf-8
import random

from redis import StrictRedis

class RedisClient(object):
    '''提供账号以及cookie新的存取操作'''
    def __init__(self, typ, website, host=REDIS_HOST, port=REDIS_PORT,
                password=REDIS_PASSWORD):
        '''
        初始化redis连接
        ：param host:地址
        ：parame port：端口
        ：param password：密码
        '''
        
        self.db = StrictRedis(host=host, port=port, password=password, 
                                decode_response=True)
        self.typ = typ
        self.website = website
    
    def name(self):
        '''
        获取hash名称
        ：return：hash名称
        '''
        
        return "{typ}:{website}".format(typ=self.typ, website=self.website)
    
    def set(self, username, value):
        '''
        设置键值对
        ：param username：用户名
        ：param value：密码或者cookie
        :return:
        '''
        
        return self.db.hset(self.name(), username, value)
    
    def get(self, username):
        '''
        根据键名获取键值
        ：param username :用户名
        ：return：
        '''
        
        return self.db.hget(self.name(), username)
        
    def delete(self, username):
        """
        删除键名删除键值对
        ：param username ：用户名
        ：return ：删除结果
        """    
        
        return self.db.hdel(self.name(), username)
        
    def count(self):
        '''
        获取数据库数量
        ：return：数目
        '''
        return self.db.hlen(self.name())
        
    def random():
        '''
        随机得到键值，用于随机Cookies函数
        ：return：随机cookies
        '''
        
        return random.choice(self.db.hvals(self.name()))
        
    def usernames(self):
        """
        获取所有账户信息
        :return:所有用户名
        """
        
        return self.db.hkeys(self.name())
        
    def all(self):
        """
        获取所有键值对
        :return:用户名和密码或cookies的映射表
        """
        
        return self.db.hgetall(self.name())
        