# -*-encoding:utf-8-*-
#CatJDInfo
import requests as rq 
url = "https://item.jd.com/6055052.html"
try:
	r = rq.get(url)
	r.raise_for_status()
	r.encoding = r.apparent_encoding
	print(r.text[:1000])
except:
	print("爬取失败！")
