# -*- coding:utf-8 -*-
import sys

from scrapy.utils.project import get_project_settings
from scrapy_universal.utils import get_config
from scrapy_universal.spiders.universal import UniversalSpider
from scrapy.crawler import CrawlerProcess

def run():
    name = sys.argv[1]
    custom_cf = get_config(name)
    # 爬取使用的spider名称
    spider = custom_cf.get("name",'universal')
    project_settings = get_project_settings()
    settings = dict(project_settings.copy())
    #合并配置
    settings.update(custom_cf.get("settings"))
    process = CrawlerProcess(settings)
    #启动爬虫
    process.crawl(spider, **{'name':name})
    process.start()
    
if __name__=='__main__':
    run()