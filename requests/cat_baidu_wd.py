#CatBaiDuWd.py
#-*- encoding:utf-8 -*-
import requests as rq 
url = "http://www.baidu.com/s"
try:
	kv = {"wd":"Python"}
	kv2 = {"user-agent":"Mozilla/5.0"}
	req = rq.get(url,params = kv,headers = kv2)
	req.raise_for_status()
	req.encoding = req.apparent_encoding
	print(req.request.headers)
	print(len(req.text))
except:
	print("抓取失败！")
