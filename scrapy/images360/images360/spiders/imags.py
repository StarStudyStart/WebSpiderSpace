# -*- coding: utf-8 -*-
import scrapy
from scrapy import Spider, Request
from urllib.parse import urlencode
import json

from images360.items import ImagesItem

class ImagsSpider(scrapy.Spider):
    name = 'imags'
    allowed_domains = ['images.so.com']
    start_urls = ['http://images.so.com/']
    
    def start_requests(self):
        base_url = 'https://image.so.com/zj?'
        data = {"ch":"photography", "listtype":"new"}
        for page in range(1, self.settings.get('MAX_PAGE') + 1):
            data['sn'] = page*30
            params = urlencode(data)
            url = base_url + params
            yield Request(url, self.parse)

    def parse(self, response):
        result = json.loads(response.text)
        for image in result.get("list"):
            item = ImagesItem()
            item['image_id'] = image.get('id')
            item['url'] = image.get('qhimg_url')
            item['title'] = image.get('group_title')
            item['thumb'] = image.get('qhimg_thumb_url')
            #self.logger.debug("item is :"+ str(item) )
            yield item
