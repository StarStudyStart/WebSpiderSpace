#-*- coding:utf-8 -*-
#CatIPInfo.py
import requests as rq 
import logging
logging.basicConfig(level=logging.INFO)
try:
	url = "http://www.ip138.com/ips138.asp?ip="
	ip_addr = "202.204.80.112" 
	req = rq.get(url + ip_addr)
	req.raise_for_status()
	req.encoding = req.apparent_encoding
	logging.info(req.text)
except:
	print("抓取失败！")
	

