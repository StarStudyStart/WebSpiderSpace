#-*- coding:utf-8 -*-
import requests
import re
import logging
import csv
logging.basicConfig(level=logging.INFO)

#获取网页
def getHtmlText(url,code='utf-8',ispic=False):
	try:
		rq = requests.get(url,headers = {"user-agent":"Mozilla/5.0"},timeout=30)
		rq.raise_for_status()
		if ispic:
			return rq.content
		rq.encoding = code
		return rq.text
	except:
		return 'something error'
		
#获取单页影片信息
def get_one_page(url,tlst):
	pageText = getHtmlText(url)
	#print(pageText)
	film_names = re.findall(r'\}\">.+?</a>',pageText)
	#print(film_names)
	film_infos = re.findall(r'star\">\n.*?\n',pageText) #star\">\n.*?\n</p> 获取不到信息  这样才是正确的star\">\n.*?\n.*？</p>
	film_scores = re.findall(r'\d\.</i><i class=\"fraction\">\d',pageText)
	film_times = re.findall(r'etime\">.*?</p>',pageText)
	filem_ranks = re.findall(r'index-\d*?\"',pageText)
	#print(film_scores)
	#print(film_infos)
	for i in range(len(film_names)):
		name = film_names[i][3:-4]
		info = film_infos[i][6:-1].strip() #正确的写法应该是这样 film_infos[i][7:-1].strip() 但是由于strip()方法 自动去掉了开头的\n 所以 6和7 实现的意义同等
		score = film_scores[i][0:2]+film_scores[i][-1]
		time = film_times[i][7:-4]
		rank = filem_ranks[i][6:-1]
		tlst.append([rank,name,info,time,score])
	print(tlst)
#数据处理，存储在csv中
def data_handle(tlst):
	#将电影宣传海报输出到csv文件中，csv不是excel 不能存储文件
	#pic = getHtmlText('http://p0.meituan.net/movie/0018b57299d0d4540330a31244c880a9112971.jpg@160w_220h_1e_1c',ispic = True)
	#with open('./pic.png','wb') as f:
	#	f.write(pic)
	try:
		with open('./top100.csv','w+',newline='') as f:
			csvWriter = csv.writer(f)
			csvWriter.writerow(['排名','电影名称','主演','上映时间','评分'])
			for star in tlst:
				csvWriter.writerow(star)
	except:
		return 'error'
			
#主函数 循环遍历前10页电影信息
def main():
	s_url = 'http://maoyan.com/board/4?offset='
	tlst = []
	#循环获取前10页相关电影信息
	for i in range(10):
		url = s_url + str(i*10)
		get_one_page(url,tlst)
	data_handle(tlst)
main()
