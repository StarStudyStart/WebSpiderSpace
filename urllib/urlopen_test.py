# coding:utf-8
import urllib.parse
import urllib.request
import socket

'''urlopen 满足基本的网页请求，可以设置timeout，传输表单数据'''
url = "https://www.python.org"
response = urllib.request.urlopen(url)
print(response.status)
print(response.read())

'''urlopen传输表单数据data,data必须进过urllib.parse转化编码 且为bytes对象类型'''
url1 = "http://httpbin.org/post"
data = bytes(urllib.parse.urlencode({"title":"Hello world!"}), encoding = "utf-8")
try:
    response1 = urllib.request.urlopen(url, data, timeout = 0.1)
    print(response1.read())
except urllib.error.URLError as e:
    if isinstance(e.reason, socket.timeout): #e.reason  scoket.timeout
        print("TIME OUT")
        
'''class urllib.request.Request(url, data=None, headers={}, origin_req_host=None, unverifiable=False, method=None)
 需要在请求中增加headers，设置useragent等参数是，需要用到另一种方式'''
headers = {
    'User-Agent': 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
    "Host":'httpbin.org'
}
data_na = {
    "name":"Yabin"
}
data = bytes(urllib.parse.urlencode(data_na), encoding="utf-8")
req = urllib.request.Request(url1, data=data, headers=headers, method="POST")
#req.add_header(headers)
res = urllib.request.urlopen(req)
print(res.read())

'''登录认证
    利用handler来构建opener'''
from urllib.request import HTTPPasswordMgrWithDefaultRealm, HTTPBasicAuthHandler, build_opener
from urllib.error import URLError

username = 'username'
password = 'password'
url = 'http://localhost:5000/'

p = HTTPPasswordMgrWithDefaultRealm()
p.add_password(None, url, username, password)
auth_handler = HTTPBasicAuthHandler(p)
opener = build_opener(auth_handler)

try:
    result = opener.open(url)
    html = result.read().decode('utf-8')
    print(html)
except URLError as e:
    print(e.reason)
    
'''proxy代理设置'''
from urllib.request import build_opener, ProxyHandler
from urllib.error import URLError
proxy_handler = ProxyHandler({
    "http":"http://127.0.0.1:9743",
    "https":"http://127.0.0.1:9743",
})
proxy_opener = build_opener(proxy_handler)
try:
    response = proxy_opener.open("http://www.baidu.com")
    print(response.read().encode("utf-8"))
except URLError as e:
    print(e.reason)
