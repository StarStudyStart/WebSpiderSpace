#CrawTaoBaoPrice.py
# -*-coding:utf:8 -*-

import re
import logging

import requests

logging.basicConfig(level=logging.INFO)

def get_html(url):
    '''get data'''
    
	try:
		rq = requests.get(url, timeout = 30)
		rq.raise_for_status()
		rq.encoding = rq.apparent_encoding
		return rq.text
	except:
		return "抓取失败"

def parse_price(ult, html):
    '''handle data'''
    
	try:
		plt = re.findall(r'\"view_price\"\:\"[\d\.]*\"', html)  # \" 将字符串标识转义成字符，这样才能对内部字符进行检索
		tlt = re.findall(r'\"raw_title\"\:\".*?\"', html)  # .* 可以匹配所有字符串，默认输出最大匹配字符串  .*? 输出最小匹配
		for i in range(len(plt)):   #java害人啊  len(plt)  写成了 plt.len()  mmp
			price = eval(plt[i].split(':')[1])
			title = eval(tlt[i].split(':')[1])
			# print(price,tlt)
			ult.append([price,title]) # 擦一个参数写错了 title  写成了  tlt
	except:
		print("error")
        

def printGoodsList(ilt):
    '''format data'''
    
	count = 0
	tplt = "{0:^4}\t{1:^10}\t{2:{3}^16}"
	print(tplt.format("序号", "price", "商品名称", chr(12288)))
	for g in ilt:
		count += 1
		print(tplt.format(count, g[0], g[1], chr(12288)))

if __name__=="__main__":
    '''
    主函数：根据货物名称搜索，然后获取信息'''
    
	goods = "书包"
	start_url = "https://s.taobao.com/search?q="
	ilt = []
	url = start_url + goods + "&s="
	deepth = 3
	for i in range(deepth):
		try:
			html = getHtml(url+str(44*i))
			# print(html)
			parsePrice(ilt,html)
		except:
			continue
	printGoodsList(ilt)

main()


