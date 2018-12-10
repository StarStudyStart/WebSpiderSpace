# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.http import HtmlResponse

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from logging import getLogger
import time

class SeleniumDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.
    def __init__(self, timeout=10):
        """初始化selenium工具"""
        self.logger = getLogger(__name__)
        self.timeout = timeout
        
        #无头的chrome浏览器
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--headless")
        self.browser = webdriver.Chrome()
        self.browser.set_window_size(1400, 700)
        self.wait = WebDriverWait(self.browser, self.timeout)

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        """
        request.url:索引页
        page:跳转界面
        根据page的数值跳转指定页面，获取数据
        """
        page = request.meta.get("page", 1)
        try:
            self.browser.get(request.url)
            if page > 1:
                self.jump_to_page(page)
            self.wait_condition(page)
            #返回当前页的源码
            return HtmlResponse(url=request.url, body=self.browser.page_source,
                request=request, encoding='utf-8',status=200)
        except TimeoutException:
            #请求超时返回状态码 500
            return HtmlResponse(url=request.url, status=500, request=request)
            
    def wait_condition(self, page):
        """
        page >= 1 时的等待条件
        """
        self.scroll_to_window_bottom(flag=5)
        self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#J_goodsList")
        ))
        self.wait.until(EC.text_to_be_present_in_element(
            (By.CSS_SELECTOR, "#J_bottomPage .p-num .curr"), str( page)
        ))
            
    def jump_to_page(self, page):
        """
        page>1 时跳转到指定页面
        """
        input_text = self.wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, "#J_bottomPage .p-skip > input")
        ))
        input_text.clear()
        input_text.send_keys(str(page))
        time.sleep(1)
        submit = self.wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, "#J_bottomPage .p-skip > a")
        ))
        submit.click()        
        
    def scroll_to_window_bottom(self,flag):
        """滑动至屏幕底部，直至所有产品都刷新出来"""
        
        for i in range(flag):
            self.browser.execute_script(
                "window.scrollTo(0, document.body.scrollHeight-100);")
            self.browser.implicitly_wait(3)
        

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)
        
    def __del__(self):
        """
        关闭测试工具
        """
        self.browser.close()
