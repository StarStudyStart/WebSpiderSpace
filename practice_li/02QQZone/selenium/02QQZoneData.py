#爬取qq历史说说
# -*- coding:utf-8 -*-
from selenium import webdriver
import requests
import time
from bs4 import BeautifulSoup

from scipy.misc import imread
import jieba
import wordcloud
import re


def login_qqzone():
    '''登陆qq空间'''
    uname = '1403913161'
    pwd = 'lyb12153719abc'
    #driver = webdriver.PhantomJS(executable_path='E:\\python_package\
    #\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
    
    driver = webdriver.Chrome()
    #设置浏览器窗口大小
    #driver.set_window_position(0,0)
    #dirver.set_window_size(1100,900)
    #少写了click()方法的 双括号‘（）’，结果老是报错Element is not currently interactableand may not be manipulated。我的脑子大概是让猪拱了浪费了我几个小时
    #加载网页
    driver.get('http://qzone.qq.com/')
    time.sleep(1)
    driver.switch_to_frame('login_frame')
    driver.find_element_by_id("switcher_plogin").click()  
    time.sleep(2)
    
    ele = driver.find_element_by_id('u')
    element = driver.find_element_by_id('p')
    element.clear()
    ele.clear()
    ele.send_keys(uname)
    element.send_keys(pwd)
    
    driver.find_element_by_id('login_button').click()
    
    driver.switch_to_window(driver.window_handles[-1])
    driver.implicitly_wait(5)
    #print(driver.page_source)
    return driver
    
def get_one_page_message(driver):
    '''获取单页的说说信息，并且存储到文件中'''
    talks = driver.find_elements_by_xpath("//div[@class='bd']/pre")
    create_time_list = driver.find_elements_by_xpath("//div[@class='ft']/\
div[@class='info']")
    with open('./talk_string.txt','a+',encoding='utf8') as f,
        open('./file_to_pic.txt','a',encoding='utf-8') as f2:
        for i in range(len(talks)):
            if talks[i].text=="":
                f.write('表情\n')
            #写入文件
            f.write(talks[i].text+'\n')
            f2.write(talks[i].text+'\n\n')
            f.write(create_time_list[i].text+'发表\n\n')
            
def get_talk_message(driver):
    '''进入qq空间查找所有的说说信息'''
    #查找’说说‘按钮并点击
    driver.find_element_by_xpath("//li/a[@title='说说']").click()
    time.sleep(5)
    
    #如果跳出弹窗关闭，不跳出则继续执行
    # suspopdWindowHandle(driver)
    
    #切换框架，否则无法查找框架下对应的元素
    driver.switch_to.frame(driver.find_element_by_xpath("//iframe[contains\
(@class,'app_canvas_frame')]"))
    #循环查找所有说说信息，并且出书为文本
    #get_one_page_message(driver)
    while True:
        get_one_page_message(driver)
        try:
            #driver.find_element_by_xpath("//div/p/sapn[@class='mod_pagenav_disable'")
            driver.find_element_by_xpath("//div/p/a[@title='下一页']").click()
            time.sleep(5)
        except:
            break
    driver.quit()
        

def suspopdWindowHandle(driver):
    '''弹窗处理'''
    try:
        popWindow = driver.find_element_by_id('qz_notification')
    except:
        return
    else:
        driver.find_element_by_xpath("//div[@id='qz_notification']\
/a[@class='op-icon icon-close']").click()
        time.sleep(3)
        

def file_data_handle():
    '''将数据整理输出为词云图片'''
    mk = imread('./fivestar.jpg')
    string_talk=""
    with open('./file_to_pic.txt','r',encoding='utf-8') as f :
        string_talk = f.read()
    w = wordcloud.WordCloud(font_path='msyh.ttc',background_color='white',width = 1000,
        height = 600,mask = mk)
    w.generate("".join(jieba.lcut(string_talk)))
    w.to_file("./talks_pic.jpg")
        
if __name__=="__main__":    
    driver = login_qqzone()
    get_talk_message(driver)
    file_data_handle()

def logined(logined_url, cookies, headers):
    pass

def login(url, username, password):
    pass
    
def detect_cookie(host,):
    global is_have_cookie
    global is_useful_cookie
    pass
    
