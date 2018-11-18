#coding:utf-8

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

browser = webdriver.Chrome()
try:
    browser.get("https://www.baidu.com")
    input_text = browser.find_element_by_id('kw')
    input_text.send_keys('python')
    input_text.send_keys(Keys.ENTER)
    wait = WebDriverWait(browser, 10)
    wait.until(EC.presence_of_element_located((By.ID, 'content_left')))

    print(browser.current_url
    print(browser.get_cookies())
    #print(browser.page_source)
finally:
    browser.close()
    