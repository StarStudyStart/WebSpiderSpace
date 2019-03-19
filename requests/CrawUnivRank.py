#CrawUnivRank.py
#-*- coding:utf-8 -*-
import time
import csv
import logging

import requests

from bs4 import BeautifulSoup
from lxml import etree
from pyquery import PyQuery as pq

logging.basicConfig(level=logging.INFO)

#get data
def get_html(url):
    try:
        rq = requests.get(url,timeout=30)
        rq.raise_for_status()
        rq.encoding = rq.apparent_encoding
        return rq.text
    except:
        print("抓取失败！") 
        return " "

#handle the data
def fill_univrList_soup(html, ulist):
    """使用beautifulsoup库进行解析"""
    
    soup = BeautifulSoup(html, "html.parser")
    for tr in soup.find('tbody').children:
        if isinstance(tr, bs4.element.Tag):
            tds = tr("td")
            ulist.append([tds[0].string, tds[1].string, tds[2].string, 
                tds[3].string])
                
def fill_univrList_pq(response, ulist):
    '''使用pyquery库进行解析'''
    html = pq(response)
    results = html('.hidden_zhpm tr').items()
    print(results)
    for tr in results:
        #tds = tr('td').text() 如果不考虑逐项存入表格的话，可以直接试用text（）输出一行文本文字 
        tds= tr('td')
        td_list = []
        for td in tds.items():
            td_list.append(td.text())
        ulist.append([td_list[0], td_list[1], td_list[2], td_list[3]])
        
def fill_univrList_xpath(response, ulist):
    '''使用xpath库进行解析'''
    html = etree.HTML(response)
    results = html.xpath('//tr[@class="alt"]')
    for tr in results:
        #'.'表示当前节点，xpath方法默认从整个html文档中查找，无论前面调用该方法的对象是什么标签。否则会从整个html文档中重新查找
        tds = tr.xpath('./td//text()') 
        ulist.append(tds[:4])
        
#foramt data && data store 
def print_univerList(ulist, num):
    tplt = "{0:^10}\t{1:{4}^10}\t{2:{4}^10}\t{3:^10}"
    # print(tplt.format("排名","大学名称","省市","总分",chr(12288)))
    
    with open('./tUniverList.csv','w+',newline='') as f: 
        csvWriter = csv.writer(f)
        csvWriter.writerow(["排名","大学名称","省市","总分"])
        for n in range(num):
            u = ulist[n]
            # if u[2] == "安徽":
            csvWriter.writerow(u)
            # time.sleep(0.01 * 5)
            # print(tplt.format(u[0],u[1],u[2],u[3],chr(12288)))

if __name__=="__main__":
    uinfo = []
    url = "http://www.zuihaodaxue.cn/zuihaodaxuepaiming2018.html"
    response = get_html(url)
    fill_univrList_xpath(response, uinfo)
    print_univerList(uinfo, 600)
