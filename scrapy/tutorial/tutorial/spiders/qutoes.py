# -*- coding: utf-8 -*-
import scrapy
from tutorial.items import QuotesItem

import logging

logging.basicConfig(level=logging.ERROR)

class QutoesSpider(scrapy.Spider): 
    name = 'qutoes'
    allowed_domains = ['quotes.toscrape.com']
    start_urls = ['http://quotes.toscrape.com/']

    def parse(self, response):
        quotes = response.css('.quote')
        #logging.info('quotes : %s' % quotes)
        for quote in quotes:
            item = QuotesItem()
            text = quote.css('.text::text').extract_first()
            item['text'] = text
            #logging.info('text: %s' % text)
            item['author'] = quote.css('.author::text').extract_first()
            item['tags'] =quote.css('.tags .tag::text').extract()
            yield item
            
        next_page = response.css('.pager .next a::attr(href)').extract_first()
        url = response.urljoin(next_page)
        yield scrapy.Request(url, callback=self.parse)
