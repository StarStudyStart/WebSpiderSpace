# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request, Spider
from weibo.items import UserItem, FollowItem
import json

class WeibocnSpider(scrapy.Spider):
    '''https://m.weibo.cn/profile/1195354434'''
    
    name = 'weibocn'
    
    user_url = "https://m.weibo.cn/profile/info?uid={uid}"
    follow_url = "https://m.weibo.cn/api/container/getSecond?containerid=100505{uid}_-_FOLLOWERS&page={page}"
    fans_url = "https://m.weibo.cn/api/container/getSecond?containerid=100505{uid}_-_FANS&page={page}"
    start_users = ['1195354434']
    
    def start_requests(self):
        for uid in self.start_users:
            yield Request(self.user_url.format(uid=uid),
                callback=self.parse)
        
    def parse(self, response):
        """解析用户id包含基本信息"""
        
        user_item = UserItem()
        user = {"user_id":"id","user_name":"screen_name",
            "avatar_hd":"avatar_hd","description":"description",
            "follow_count":"follow_count","followers_count":"followers_count",
            "gender":"gender","verified":"verified",
            "verified_reason":"verified_reason"}
        user_info = json.loads(response.text).get("data").get("user")
        for key,attr in user.items():
            user_item[key] = user_info.get(attr)
        yield user_item
        
        page_init = self.settings.get("PAGE_INIT")
        uid = user_info.get("id")
        #关注
        yield Request(self.follow_url.format(uid=uid,page=page_init),
                callback=self.parse_follow,meta={'uid':uid})
                
        #粉丝
        yield Request(self.fans_url.format(uid=uid,page=page_init),
                callback=self.parse_follow,meta={'uid':uid})
                
    def parse_follow(self, response):
        """解析用户的关注列表"""
        
        #获取当前页面数以及当前爬取用户id
        uid = response.meta.get("uid")
        page = json.loads(response.text).get("data").get("cardlistInfo").get("page")
        
        follow_item = FollowItem()
        follows = {"follow_id":"id","user_name":"screen_name",
            "description":"description"}
        follow_info = json.loads(response.text).get("data").get("cards")
        
        if follow_info:
            for user_list in follow_info:
                user_info = user_list.get("user")
                for key, attr in follows.items():
                    follow_item[key] = user_info.get(attr)
            yield follow_item
                
            #添加下一页列表
            yield Request(self.follow_url.format(uid=uid,page=page),
                callback=self.parse_follow,meta={"uid":uid})
        
    def parse_fans(self, response):
        """解析用户的粉丝列表"""
        pass
        
    def get_follows_fans_data(item,response,type_data):
        #获取当前页面数以及当前爬取用户id
        uid = response.meta.get("uid")
        if type_data == "follow":
            data = {"follow_id":"id","user_name":"screen_name",
                "description":"description"}
        if type_data == "fans":
            data = {"fans_id":"id","user_name":"screen_name",
                "description":"description"}
        info = json.loads(response.text).get("data").get("cards")
        
        if info:
            for user_list in follow_info:
                user_info = user_list.get("user")
                for key, attr in data.items():
                    item[key] = user_info.get(attr)
            return item
