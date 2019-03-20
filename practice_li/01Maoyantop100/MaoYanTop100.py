#-*- coding:utf-8 -*-
import requests
import re
import logging
import csv

logging.basicConfig(level=logging.ERROR)


def get_html_text(url,code='utf-8',ispic=False):
    '''获取网页信息'''
    
    try:
        rq = requests.get(url,headers = {"user-agent":"Mozilla/5.0"},timeout=30)
        rq.raise_for_status()
        if ispic:
            return rq.content
        rq.encoding = code
        return rq.text
    except:
        return 'something error'
        

def get_one_page(url,tlst):
    '''获取单页影片信息'''
    
    page_text = get_html_text(url)
    pattern = re.compile('<dd>.*?board-index.*?>(.*?)</i>.*?.*?data-src="(.*?)".*?<a href.*?title.*?data-val.*?>(.*?)</a>.*?star">(.*?)</p>.*?releasetime">(.*?)</p>.*?integer">(.*?)</i>.*?fraction">(.*?)</i>', re.S)
    items = re.findall(pattern, page_text)
    logging.info("result is %s" % items)
    
    for item in items:
        tlst.append([item[0], item[2], item[3].strip()[3:], item[4].strip()[5:],
            item[5]+item[6]])
        '''
        为了便于处理庞大的数据，以生成器方式返回数据节省内存空间    
        yield {
            'index':item[0],
            'image':item[1],
            'title'：item[2].strip(),
            'stars':item[3].strip()[3:],
            'time':item[4].strip()[5:],
            'score':item[5].strip() + item[6].strip()
        }'''
    

def data_handle(tlst):
    '''数据处理，存储在csv中
    #将电影宣传海报输出到csv文件中，csv不是excel 不能存储文件
    #pic = getHtmlText('http://p0.meituan.net/movie/0018b57299d0d4540330a31244c880a9112971.jpg@160w_220h_1e_1c',ispic = True)
    #with open('./pic.png','wb') as f:
    #   f.write(pic)'''

    with open('./top100.csv','w+',newline='') as f:
        csvWriter = csv.writer(f)
        csvWriter.writerow(['排名','电影名称','主演','上映时间','评分'])
        for star in tlst:
            csvWriter.writerow(star)
            

if __name__=="__main__":
    '''主函数 循环遍历前10页电影信息'''
    s_url = 'http://maoyan.com/board/4?offset='
    tlst = []
    
    #循环获取前10页相关电影信息
    for i in range(10):
        url = s_url + str(i*10)
        get_one_page(url, tlst)
        logging.info("result is %s" % tlst)
    data_handle(tlst)
