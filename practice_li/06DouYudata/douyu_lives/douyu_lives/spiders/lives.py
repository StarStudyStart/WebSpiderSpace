# -*- coding: utf-8 -*-
import scrapy


class LivesSpider(scrapy.Spider):
    name = 'lives'
    allowed_domains = ['www.douyu.com/directory/all']
    start_urls = ['http://www.douyu.com/directory/all/']

    def parse(self, response):
        self.logger.debug(response.text)
        pass
