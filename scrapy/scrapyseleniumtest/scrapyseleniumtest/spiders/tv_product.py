# -*- coding: utf-8 -*-
import scrapy
from scrapy import Request
from scrapyseleniumtest.items import ProductItem

from urllib.parse import quote


class TvProductSpider(scrapy.Spider):
    name = 'tv_product'
    
    def __init__(self, keyword, max_page):
        self.keyword = keyword
        self.max_page = max_page
        self.base_url = 'https://search.jd.com/Search?keyword='
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            keyword = crawler.settings.get('KEY_WORD'),
            max_page = crawler.settings.get('MAX_PAGE'),
        )
    
    def start_requests(self):
        '''编辑链接'''
        for page in range(1, self.max_page + 1):
            url = self.base_url + quote(self.keyword)+'&enc=utf-8'
            yield Request(url, callback=self.parse, meta={'page':page},
                dont_filter=True)

    def parse(self, response):
        #self.logger.debug(response.text)
        """
        解析网页返回数据
        """
        products = response.xpath('//div[@id="J_goodsList"]/ul/li')
        item = ProductItem()
        for product in products:
            item['image'] = "".join(product.xpath(
                './div/div[@class="p-img"]/a/@href').extract()).strip()
            name = "".join(product.xpath(
                './div/div[contains(@class,"p-name")]//text()'
                ).extract()).strip()
            item['title'] = name.replace('\t','').replace('\n','')
            item['price'] = "".join(product.xpath(
                './div/div[@class="p-price"]/strong//text()'
                ).extract()).strip()
            item['deal'] = "".join(product.xpath(
                './div/div[@class="p-commit"]/strong//text()'
                ).extract()).strip()
            item['shop'] = "".join(product.xpath(
                './div/div[@class="p-shop"]//a/text()').extract()).strip()
            yield item
        
