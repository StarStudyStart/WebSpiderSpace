# -*- coding: utf-8 -*-
import scrapy
import re


class WeatherSpider(scrapy.Spider):
    name = 'weather'
    start_urls = ['http://mobile.weather.com.cn/js/citylist.xml']

    def parse(self, response):
        self.count = 0
        for codeList in response.css('d').extract():
            if self.count >= 40:
                    break
            try:
                weather_code = re.findall(r'\"\d{9}\"',codeList)[0][1:-1]
                url = 'http://wthrcdn.etouch.cn/WeatherApi?citykey='+weather_code #int 类型不能和str拼接
                self.count = self.count+1
                yield scrapy.Request(url,callback = self.parse_weather)
            except:
                continue
    def parse_weather(self,response):
        infoDict = {}
        city = response.css('city').extract()[0][6:-7]   #extract() 返回的列表类型 [0] 返回列表之后的第一个值
        wendu = response.css('wendu').extract()[0][7:-8]
        fengxiang = response.css('fengxiang').extract()[0][11:-12]
        infoDict.update({'城市':city,'温度':wendu+'℃','风向':fengxiang})
        yield infoDict


