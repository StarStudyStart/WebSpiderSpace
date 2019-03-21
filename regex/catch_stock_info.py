#CrawStockInfo.py
#-*- coding:utf-8 -*-
import re
import traceback

import requests
from bs4 import BeautifulSoup


def get_html(url, code = 'utf-8'):
    '''获取页面信息'''
    
    try:
        rq = requests.get(url, timeout = 30)
        rq.raise_for_status()
        rq.encoding = code
        return rq.text
    except:
        return "something wrong"
        
def get_stocklist(slist, htmlUrl):
    '''获取股票列表，组成访问股票信息的url'''
    
    html = get_html(htmlUrl, 'GB2312')
    soup = BeautifulSoup(html, "html.parser")
    a = soup.find_all("a")
    for i in a :
        try:
            href = i.attrs["href"]
            slist.append(re.findall(r'[s][zh]\d{6}', href)[0]) #findall 返回列表类型,匹配不到则返回空列表，此时findall()[0] 出现指针异常
        except: #增加Try..except是为了达到如下效果：href为空时，直接跳出循环；href不为空，但是不匹配regex时，直接调到下次循环...保证slist中不会出现空列表；
            continue


def get_stockinfo(slist, stock_url,fpath):
    '''访问股票列表代码网页，提取其中相关信息并存储到文件中'''
    
    count = 0
    for end_url in slist:
        # if end_url == "":
        #   continue
        url = stock_url + end_url + ".html"
        html = get_html(url)
        try:
            if html == "":
                continue
            stock_info_dict  = {}
            soup = BeautifulSoup(html, "html.parser")
            stockInfo = soup.find('div', attrs={'class':'stock-bets'})
            if type(stockInfo) == None:
                continue
            name = stockInfo.find_all('a', attrs={'class':'bets-name'})[0]
            stock_info_dict.update({'股票名称':name.text.split()[0]})

            keyList = stockInfo.find_all('dt')
            valueList = stockInfo.find_all('dd')
            
            for i in range(len(keyList)):
                key = keyList[i].text
                value = valueList[i].text
                stock_info_dict[key] = value
                
            with open(fpath, 'a', encoding="utf-8") as f:
                f.write(str(stock_info_dict) + '\n')
                count += 1
                print('\r当前进度：{:.2f}%'.format(count * 100 / len(slist)), end=' ')
        except:
            print('\r当前进度：{:.2f}%'.format(count * 100 / len(slist)), end=' ')
            continue
            

if __name__=="__main__":
    '''主函数'''
    
    slist = []
    output_path = "D:/stock_info.txt"
    stock_list_url = "http://quote.eastmoney.com/stocklist.html"
    stock_info_url = "http://gupiao.baidu.com/stock/"
    get_stocklist(slist, stock_list_url)
    # print(slist)
    get_stockinfo(slist, stock_info_url, output_path)


