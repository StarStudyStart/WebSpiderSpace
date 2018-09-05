# -*- coding:utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup
import random
import datetime

random.seed(datetime.datetime.now())

def getHtml(article_url):
    try:
        rq = requests.get('http://en.wikipedia.org'+article_url,timeout =30)
        rq.raise_for_status()
        rq.encoding = rq.apparent_encoding
        return rq.text 
    except:
        print('出了一点小错误！')

def getLinks(article_url):
    html = getHtml(article_url)
    soup = BeautifulSoup(html,'html.parser')
    return soup.find('div',{'id':'bodyContent'}).find_all('a',href = re.compile('^(/wiki/)((?!:).)*$'))

def getHistoryIps(pageUrl):
    # format of history page is :https://en.wikipedia.org/w/index.php?title= title_in_url &action=history
    pageUrl = pageUrl.replace('/wiki/','')
    historyUrl = '/w/index.php?title='+pageUrl+'&action=history'  
    print('history url is:'+historyUrl)
    html2 = getHtml(historyUrl)  #gethtml 中已经预留了前置连接所以history 不需要增加http://en.wikipedia.org从我你塞因为这个东西浪费了一下午
    soup = BeautifulSoup(html2,'html.parser')
    addresses = soup.find_all('a',{'class':'mw-anonuserlink'})
    addressList = set()
    for address in addresses:
        addressList.add(address.text)
    return addressList

links = getLinks('/wiki/Python_(programming_language)')

while(len(links)>0):
    for link in links:
        print('--------------------------')
        historyIps = getHistoryIps(link.attrs['href'])
        for historyIp in historyIps:
            print(historyIp)
    newLink = links[random.randomint(0,len(links))]
    newLinks = getLinks(newLink)


# def main():
#     article_url = '/wiki/Python_(programming_language)'
#     html = getHtml(article_url)
#     print(html)
#     parse_html(html)

# main()
