#coding:utf-8

import requests
from lxml import etree 

class Login(object):
    def __init__(self):
        self.headers = {
            'Referer':'https://github.com/',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36',
            'Host':'github.com',
        }
        self.login_url = 'https://github.com/login'
        self.post_url = 'https://github.com/session'
        self.logined_url = 'https://github.com/settings/profile'
        self.session = requests.Session()
        
    def token(self):
        response = self.session.get(self.login_url, headers=self.headers)
        html = etree.HTML(response.text)
        self.token = html.xpath('//div//input[2]/@value')[0]
        return self.token
        
    def login(self, email, password):
        post_data = {
            'commit': 'Sign in',
            'utf8': '✓',
            'authenticity_token': self.token(),
            'login': email,
            'password': password,
        }
        response = self.session.post(self.post_url, 
            data=post_data, headers=self.headers)
            
        reponse = self.session.get(self.logined_url,headers=self.headers)
        print(response.text)
if __name__=='__main__':
    email = '18792146966@163.com'
    password = 'lyb12153719'
    login = Login().login(email,password)
        