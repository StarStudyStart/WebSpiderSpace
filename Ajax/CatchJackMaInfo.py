#coding:utf-8
import requests
from urllib.parse import urlencode
from pyquery import PyQuery as pq
import pymongo

client = pymongo.MongoClient(host='localhost', port=27017) # host 名字打错了，结果存储的时候一直报错，我也是醉了  localhost 打成loaclhost
db = client['weibo']
collection = db['jackma_info']
max_page= 158//9 + 1

def get_page(page):
    '''获取马云爸爸的微博信息'''
    
    base_url = 'https://m.weibo.cn/api/container/getIndex'
    
    params = {
        'type':'uid',
        'value':'2145291155',
        'containerid':'1076032145291155',
        'page':page,
    }
    
    headers = {
        'Host':'m.weibo.cn',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        'Referer': 'https://m.weibo.cn/u/2145291155',
        'X-Requested-With':'XMLHttpRequest',
    }
    #url = base_url + urlencode(params)
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.ConnectionError as e:
        print('Error:',e.args)

def parse_page(json):
    '''解析数据,构造生成器'''
    if json:
        items = json.get('data').get('cards') # 直接使用get('cards')无法获取信息
        for item in items:
            item = item.get('mblog')
            weibo = {}
            weibo['text'] = pq(item.get('text')).text().strip()
            weibo['id'] = item.get('id')
            weibo['time'] = item.get('created_at')
            weibo['attitudes'] = item.get('attitudes_count')
            weibo['comments'] = item.get('comments_count')
            weibo['reposts'] = item.get('reposts_count')
            yield weibo
    
def save_to_mongo(result):
    '''将信息存储到mongo数据库中'''
    if collection.insert_one(result):
        print('Saved to mongo!')

if __name__ == '__main__':
    for page in range(1,max_page+1):
        json = get_page(page)
        results = parse_page(json)
        for result in results:
            print(result)
            save_to_mongo(result)
