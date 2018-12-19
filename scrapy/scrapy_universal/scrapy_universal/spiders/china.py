# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

from scrapy_universal.items import NewsItem
from scrapy_universal.loader import ChinaLoader

class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    start_urls = ['https://tech.china.com/articles/']

    rules = (
        Rule(LinkExtractor(allow=r'article\/.*\.html$',
            restrict_xpaths='//div[@id="left_side"]//div[@class="con_item"]',
            unique=True),callback='parse_item', follow=True),
        Rule(LinkExtractor(
            restrict_xpaths='//div[@id="pageStyle"]//a[contains(.,"下一页")]')),
    )
    '''
    def parse_item(self, response):
        item = NewsItem()
        item['title'] = response.css('#chan_newsTitle ::text').extract_first()
        item['url'] = response.url
        item['text'] = ''.join(
            response.css('#chan_newsDetail ::text').extract())strip()
        item['datetime'] = response.css('#chan_newsInfo::text'
            ).re_first(r'\d{4}-\d+-\d+\s\d+:\d+:\d+')
        item['source'] = response.css('#chan_newsInfo::text'
            ).re_first(r'来源：(.*)').strip()
        item['website'] = '中华网'
        #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        #i['name'] = response.xpath('//div[@id="name"]').extract()
        #i['description'] = response.xpath('//div[@id="description"]').extract()
        yield item
    '''
    def parse_item(self, response):
        loader = ChinaLoader(item=NewsItem(), response=response)
        loader.add_css('title', '#chan_newsTitle ::text')
        loader.add_value('url', response.url)
        loader.add_css('text', '#chan_newsDetail ::text')
        loader.add_css('datetime', '#chan_newsInfo ::text',
            re='\d{4}-\d+-\d+\s\d+:\d+:\d+')
        loader.add_css('source', '#chan_newsInfo::text',
            re='来源：(.*)')
        loader.add_value('website','中华网')
        
        yield loader.load_item()
        