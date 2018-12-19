# -*- coding: utf-8 -*-
import scrapy
from scrapy_splash import SplashRequest
from scrapy_splash_test.items import ProductItem

from urllib.parse import quote


class ProductSpider(scrapy.Spider):
    name = 'jd'

    script="""
    function main(splash, args)
      splash.images_enabled = false
      assert(splash:go(args.url))
      assert(splash:wait(args.wait))
      js = string.format("document.querySelector('#J_bottomPage .p-skip > input').value=%d;document.querySelector('#J_bottomPage .p-skip > a').click()",args.page)
        splash:evaljs(js)
        assert(splash:wait(args.wait))
      return splash:html()
    end
    """

    def __init__(self, keyword, max_page):
        self.keyword = keyword
        self.max_page = max_page
        self.base_url = 'https://search.jd.com/Search?keyword='

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            keyword=crawler.settings.get('KEY_WORD'),
            max_page=crawler.settings.get('MAX_PAGE'),
        )

    def start_requests(self):
        '''编辑链接'''
        for page in range(1, self.max_page + 1):
            url = self.base_url + quote(self.keyword) + '&enc=utf-8'
            yield SplashRequest(url, callback=self.parse, endpoint='execute',args={'lua_source':ProductSpider.script,'page':page,
                                                                                   'wait':7})
    def parse(self, response):
        # self.logger.debug(response.text)
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
            item['title'] = name.replace('\t', '').replace('\n', '')
            item['price'] = "".join(product.xpath(
                './div/div[@class="p-price"]/strong//text()'
            ).extract()).strip()
            item['deal'] = "".join(product.xpath(
                './div/div[@class="p-commit"]/strong//text()'
            ).extract()).strip()
            item['shop'] = "".join(product.xpath(
                './div/div[@class="p-shop"]//a/text()').extract()).strip()
            yield item

