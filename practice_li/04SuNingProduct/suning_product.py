#coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from urllib.parse import quote 
from pyquery import PyQuery
import time
from pymongo import MongoClient
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--headless')
browser = webdriver.Chrome() #chrome_options=chrome_options
wait = WebDriverWait(browser, 10)

KEYWORD = '荣耀'

def index_page(page):
    '''
    索引界面
    ：param page:页码
    '''
    print("正在爬取第", page, '页')
    url = 'https://search.suning.com/'+quote(KEYWORD)+'/'
    browser.get(url)
    #browser.add_cookie('')
    if page>1:
        """
        获取页码控件以及submit控件
        """
        input_text = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, '#bottomPage')))
        input_text.clear()
        input_text.send_keys(str(page))
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, '.page-more.ensure' )))
        submit.click()
        time.sleep(2)
        
    wait.until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR, '#product-wrap #product-list ul.general li'))
    )
    browser.implicitly_wait(5)
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, '#bottom_pager .cur'))
    )
    # 模拟下滑到底部操作
    for i in range(1, 3):
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight-100);")
        time.sleep(1)
    get_products()
        
def get_products():
    '''解析产品'''
    doc = PyQuery(browser.page_source)
    items = doc('#product-list ul.general li').items()
    for item in items:
        product = {
            'price':item.find('.res-info .price-box .def-price').text(),
            'title':item.find('.res-info .title-selling-point a').text(),
            'count':item.find('.res-info .info-evaluate a').text(),
        }
        print(product)
        save_to_mongo(product)

def save_to_mongo(result):
    '''将处理后的结果存储到mongodb中'''
    
    MONGO_URL = 'localhost'
    MONGO_DB = 'suning'
    MONGO_COLLECTION = 'honor'
    
    client = MongoClient(MONGO_URL)
    db = client[MONGO_DB]
    
    try:
        if db[MONGO_COLLECTION].insert_one(result):
            print('saved successful')
    except:
        print('存储到MongoDB失败！')
    
def main():
    
    MAX_PAGE=4
    
    for i in range(1, MAX_PAGE):
        index_page(i)
    browser.close()
    
if __name__ =='__main__':
    main()