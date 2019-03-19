# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class WeiboItem(Item):
    comments_count = Field()
    created_at = Field()
    obj_ext = Field()
    text = Field()
    raw_text = Field()
    
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
    fans_id = Field()
    
