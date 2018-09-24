#CrawUnivRank.py
#-*- coding:utf-8 -*-
import requests
from bs4 import BeautifulSoup
import bs4
import time
import csv

#get data
def getHTML(url):
	try:
		rq = requests.get(url,timeout=30)
		rq.raise_for_status()
		rq.encoding = rq.apparent_encoding
		print(rq.apparent_encoding)
		return rq.text
	except:
		print("抓取失败！") 
		return " "

#handle the data
def fillUnivrList(html,ulist):
	soup = BeautifulSoup(html,"html.parser")
	for tr in soup.find('tbody').children:
		if isinstance(tr,bs4.element.Tag):
			tds = tr("td")
			ulist.append([tds[0].string,tds[1].string,tds[2].string,tds[3].string])

#foramt data && data store 
def printUniverList(ulist,num):
	tplt = "{0:^10}\t{1:{4}^10}\t{2:{4}^10}\t{3:^10}"
	# print(tplt.format("排名","大学名称","省市","排名积分",chr(12288)))

	with open('./tUniverList.csv','w+',newline='') as f: 
		csvWriter = csv.writer(f)
		csvWriter.writerow(["排名","大学名称","省市","排名积分"])
		for n in range(num):
			u = ulist[n]
			# if u[2] == "安徽":
			csvWriter.writerow(u)
			# time.sleep(0.01*5)
			# print(tplt.format(u[0],u[1],u[2],u[3],chr(12288)))

def main():
	unifo = []
	url = "http://www.zuihaodaxue.cn/zuihaodaxuepaiming2018.html"
	html = getHTML(url)
	fillUnivrList(html,unifo)
	printUniverList(unifo,600)
main()
