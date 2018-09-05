# javascript 重定向
#-*- coding:utf-8 -*-
from selenium import webdriver
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import StaleElementReferenceException
import time

ps_path = 'E:\\python_package\\phantomjs-2.1.1-windows\
\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe'
url = 'http://pythonscraping.com/pages/javascript/redirectDemo1.html'

def waitForLoad(driver):
	elem = driver.find_element_by_tag_name('html')
	count = 0
	while True:
		count +=1
		if count>20:
			print('Timing out after 10 seconds and returning')
			return
		time.sleep(.5)
		try:
			elem == driver.find_element_by_tag_name('html')
		except StaleElementReferenceException:
			return
	
driver = webdriver.PhantomJS(executable_path=ps_path) #获取对象内容
driver.get(url) #加载页面js内容
waitForLoad(driver) #等待获取js跳转后的页面内容
print(driver.page_source) 
	
