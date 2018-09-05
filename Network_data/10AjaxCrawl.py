#ajax 异步页面数据获取
from selenium import webdriver
import time
driver = webdriver.PhantomJS(executable_path='E:\\python_package\\phantomjs-2.1.1-windows\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe')
driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")
time.sleep(3)
print(driver.find_element_by_id('content').text)
driver.close()
