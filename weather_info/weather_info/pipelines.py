# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


class WeatherInfoPipeline(object):
    def process_item(self, item, spider):
        return item
class WeatherInfoPipeline_1(object):
    def open_spider(self,spider):   #open_spider 写成start_spider  我也是服了自己
        self.f = open('weather.txt','w')  
    def close_spider(self,spider): # close 写错
        self.f.close()
    def process_item(self ,item,spider):  # 方法名写错 process_spider
        try:
            line = str(dict(item))+'\n'
            self.f.write(line)
        except:
            pass
        return item
