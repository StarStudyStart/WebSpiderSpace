# -*- coding: utf-8 -*-
import scrapy


class LogTalkSpider(scrapy.Spider):
    name = 'log_talk'
    allowed_domains = ['https://qzone.qq.com']
    start_urls = ['https://qzone.qq.com/']

    def parse(self, response):
        response.css("#")
        pass
