#coding: utf-8
import requests

url = ''

params = {
    '':'',
}

def get_page(offset, url):
    '''获取路人街拍所有页面'''
    pass
    
def get_images(json):
    '''获取所有图片链接'''
    pass
    
def save_images():
    '''循环请求图片链接，获取图片存储到本地'''
    pass
    
def main(offset):
    json = get_page(offset, url)
    for item in get_images(json):
        print(item)
        save_image(item)
        
        
    