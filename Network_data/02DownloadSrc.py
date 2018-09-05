#-*- coding:utf-8 -*-
from urllib.request import urlretrieve
from urllib.request import urlopen
from bs4 import BeautifulSoup
import os

downloadDirectory = 'downliaded/'
baseUrl = 'http://pythonscraping.com'

def getAbsoluteURL(baseUrl, source):
	if source.startswith("http://www."):
		url = "http://"+source[11:]
	elif source.startswith("http://"):
		url = source
	elif source.startswith("www."):
		url = source[4:]
		url = "http://"+source
	else:
		url = baseUrl+"/"+source
	if baseUrl not in url:
		return None
	return url
	
def getDownLoadPath(baseUrl,absoluteUrl,downloadDirectory):
	path = absoluteUrl.replace('www.','')
	path = path.replace(baseUrl,'')
	path = downloadDirectory+path
	directory = os.path.dirname(path)
	
	if not os.path.exists(directory):
		os.makedirs(directory)
	return path
	
	

html = urlopen('http://www.pythonscraping.com')
bsObj = BeautifulSoup(html,'html.parser')
downList = bsObj.find_all(src=True)


for down in downList:
	fileUrl = getAbsoluteURL(baseUrl,down.attrs['src'])
	if fileUrl is not None:
		print(fileUrl)

urlretrieve(fileUrl,getDownLoadPath(baseUrl,fileUrl,downloadDirectory)) #下载最后一个src连接的图片  
