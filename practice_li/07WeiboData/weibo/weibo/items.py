# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class WeiboItem(Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass
    
class UserItem(Item):
    
    user_id = Field()
    avatar_hd = Field()
    description = Field()
    follow_count = Field()
    followers_count = Field()
    gender = Field()
    user_name = Field()
    verified = Field()
    verified_reason = Field()
    
class FollowItem(UserItem):
    page = Field()
    follow_id = Field()
    
class FansItem(UserItem):
    pass
