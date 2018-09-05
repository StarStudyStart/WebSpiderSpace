# -*- coding: utf-8 -*-
# import scrapy
# import logging
# import re
# # logging.basicConfig(level = logging.INFO)
# class StocksSpider(scrapy.Spider):
#     name = 'stocks'
#     start_urls = ['http://quote.eastmoney.com/stocklist.html']

#     def parse(self, response):
#     	for href in response.css('a::attr(href)').extract():
#             try:
#                 stock = re.findall(r'[s][hz]\d{6}',href)[0]
#                 url = 'http://gupiao.baidu.com/stock/'+stock+'.html'
#                 # logging.info('url is %s', % url)
#                 yield scrapy.Request(url,callback = self.parse_stock)
#             except:
#                 continue
#     def parse_stock(self,response):
#         infoDict = {}
#         stock_info = response.css('.stock-bets')
#         name = stock_info.css('.bets-name').extract()[0]
#         keyList = stock_info.css('dt').extract()
#         valueList = stock_info.css('dd').extract()
#         print(keyList+"\n")
#         for i in range(len(keyList)):
#             key = re.findall(r'>.*</dt>',keyList[i])[0][1:-5]
#             print('key is '+key)
#             try:
#                 value = re.findall(r'\d+\.?.*</dd>',valueList[i])[0][0:-5]
#             except:
#                 val = '--'
#             infoDict[key] = value
#         infoDict.update({'股票名称':re.findall('\s.*\(',name)[0].split()[0] + \
#              re.findall('\>.*\<', name)[0][1:-1]})
#         yield infoDict

import scrapy
import re
 
 
class StocksSpider(scrapy.Spider):
    name = "stocks"
    start_urls = ['http://quote.eastmoney.com/stocklist.html']
 
    def parse(self, response):
        for href in response.css('a::attr(href)').extract():
            try:
                stock = re.findall(r"[s][hz]\d{6}", href)[0]
                url = 'http://gupiao.baidu.com/stock/' + stock + '.html'
                yield scrapy.Request(url, callback=self.parse_stock)
            except:
                continue
 
    def parse_stock(self, response):
        infoDict = {}
        stockInfo = response.css('.stock-bets')
        name = stockInfo.css('.bets-name').extract()[0]
        keyList = stockInfo.css('dt').extract()
        valueList = stockInfo.css('dd').extract()
        for i in range(len(keyList)):
            key = re.findall(r'>.*</dt>', keyList[i])[0][1:-5]
            try:
                val = re.findall(r'\d+\.?.*</dd>', valueList[i])[0][0:-5]
            except:
                val = '--'
            infoDict[key]=val
 
        infoDict.update(
            {'股票名称': re.findall('\s.*\(',name)[0].split()[0] + \
             re.findall('\>.*\<', name)[0][1:-1]})
        yield infoDict