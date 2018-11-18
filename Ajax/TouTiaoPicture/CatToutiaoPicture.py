#coding: utf-8
'''这样爬取的仅是缩略图，改进后爬取实际图片'''
import requests
import time
from hashlib import md5
import os 
from multiprocessing.pool import Pool

url = 'https://www.toutiao.com/search_content/'

def get_page(offset, url):
    '''获取路人街拍所有页面'''
    params = {
        'offset':offset,
        'format':'json',
        'keyword':'路人街拍',
        'autoload':'true',
        'count':'20',
        'cur_tab':'1',
        'from':'search_tab',
    }
    headers = {
        'Host':'www.toutiao.com',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
        #'Referer': 'https://www.toutiao.com/search/?keyword=%E8%B7%AF%E4%BA%BA%E8%A1%97%E6%8B%8D',
        'X-Requested-With':'XMLHttpRequest',
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.ConnectionError:
        return None
    
def get_images(json):
    '''获取所有图片链接'''
    if json.get('data'):
        for item in json.get('data'):
            title = item.get('title')
            images = item.get("image_list")
            print(images)
            if images: #部分获取不到images
                for image in images:
                    image_url =image.get('url')
                    yield {
                        'title':title,
                        'image_url':image_url,
                    }
    
def save_image(item):
    '''请求图片链接，获取图片存储到本地'''
    base_url = "https:"
    if not os.path.exists(item.get('title')):
        os.mkdir(item.get('title'))
    try:
        url = base_url + item.get('image_url')
        response = requests.get(url)
        file_path = '{0}/{1}{2}'.format(item.get('title'), md5(response.content).hexdigest(), '.jpg')
        if not os.path.exists(file_path):
            with open(file_path, 'wb') as f:
                f.write(response.content)
        else :
            print('Already Downloaded', file_path)
    except:
        print('Failed to save image')
        
def main(offset):
    json = get_page(offset, url)
    for item in get_images(json):
        print(item)
        save_image(item)
        
if __name__ == '__main__':
    
    GROUPSTART = 1
    GROUPEND = 20
    
    pool = Pool()
    groups = [ x*20 for x in range(GROUPSTART,GROUPEND + 1)]
    pool.map(main, groups)
    pool.close()
    pool.join()
    
    
        
        
    