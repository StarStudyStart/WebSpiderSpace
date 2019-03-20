# !/usr/bin/env python3.7
#-*- encoding:utf-8 -*-
# CaAMZInfo.py
import requests as rq 
url = "https://www.amazon.cn/dp/B00QJDOLIO"
try :
	req  = rq.get(url,headers = {"user-agent":"Mozilla/5.0"})
	req.raise_for_status()
	req.encoding = req.apparent_encoding
	print(req.text[1000:2000])
	print(req.request.headers)
except:
	print("抓取失败！")
