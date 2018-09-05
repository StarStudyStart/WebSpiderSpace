#！/usr/bin/env python3
#-*- coding:utf-8 -*-
import requests as rq
import os
url = "https://www.nationalgeographic.com/content/dam/environment/2018/07/trump-ocean-policy/01-trumps-ocean-policy-nationalgeographic_2461163.adapt.1900.1.jpg"
root = "E://pic//"
path = root + url.split("/")[-1]
try:
	if not os.path.exists(root):
		os.mkdir(root)
	if not os.path.exists(path):
		req = rq.get(url)
		req.raise_for_status()
		req.enconding = req.apparent_encoding
		with open(path,'wb') as f:
			f.write(req.content)
			f.close()
			print("file saved successfully!")
	else:
		print("file is exists!")
except:
	print("抓取失败！")
