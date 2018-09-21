#读取亚马逊图书预览的文字图片并且转化为相关文字文件输出
from selenium import webdriver
from urllib.request import urlretrieve
import time
import subprocess
phan_path = 'E:\\python_package\\phantomjs-2.1.1-windows\
\\phantomjs-2.1.1-windows\\bin\\phantomjs.exe'
firefox_path = 'E:\\ProgramFiles_x86\\Firefox\\geckodriver-v0.21.0-win64\\geckodriver.exe'
chrome_path = 'C:\Program Files (x86)\Google\Chrome\Application'
#driver = webdriver.PhantomJS(executable_path=phan_path)
driver = webdriver.Chrome()
time.sleep(2)
driver.get('http://www.amazon.com/War-Peace-Leo-Nikolayevich-Tolstoy/dp/1427030200')
#等待页面加载
time.sleep(2)
#点击预览图书按钮sitbLogoImage
driver.find_element_by_id('sitbLogoImg').click()
imageList = set()
#等待页面加载完成
time.sleep(6)
#当右箭头可以点击时开始翻页
while 'pointer' in driver.find_element_by_id('sitbReaderRightPageTurner').get_attribute('style'):
	driver.find_element_by_id('sitbReaderRightPageTurner').click()
	time.sleep(3)
	pages = driver.find_elements_by_xpath("//div[@class='pageImage']/div/img")
	for page in pages:
		src= page.get_attribute("src")
		imageList.add(src)
driver.quit()

for image in sorted(imageList):
	urlretrieve(image,'page.jpg')
	p = subprocess.Popen(['tesseract','page.jpg','page'],stdout=subprocess.PIPE,
	stderr = subprocess.PIPE)
	p.wait()
	f = open('page.txt','r',encoding='utf-8')
	print(f.read())



