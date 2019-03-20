#coding:utf-8
import requests
import re

url = "https://www.zhihu.com/explore"
url1= "https://github.com/favicon.ico"
url2 = "http://httpbin.org/post"

data = {
    "name":"gemey",
    "pwd":123456,
}

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36\
        (KHTML,like Gecko) Chrome/70.0.3538.67 Safari/537.36",
}

#抓取普通网页 get
try:
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    pattern = re.compile('explore-feed.*?question_link.*?>(.*?)</a>', re.S)
    titles = re.findall(pattern, res.text)
    print(titles)
except:
    print("抓取失败")
    
#抓取图片
def get_picture():
    try:
        res1 = requests.get(url1)
        res1.raise_for_status()
        #print(res1.text)
        #print(res1.content)
        with open("git_ico.ico", 'wb') as f:
            f.write(res1.content)
    except:
        print("抓取失败。")

#提交表单数据
try:
    res2 = requests.post(url2, data=data)
    res2.raise_for_status()
    print(res2.text)
    print(res2.json())
except:
    print("抓取失败！")

#文件上传
files = {
    "file":open("git_ico.ico", 'rb'),
}
try:
    res3 = requests.post(url2, files=files)
    res3.raise_for_status()
    print(res3.text)
except:
    print("文件上传失败!")
    
#获取responsecookie
res4 = requests.get("https://www.baidu.com")
print(res4.cookies)
for key, value in res4.cookies.items():
    print(key+'='+value)
#利用cookie维持登录状态
headers1 = {
    'Cookie': 'BAIDUID=2005CE00AD6B3E2CAB4B06409ECD1D79:FG=1; BIDUPSID=2005CE00AD6B3E2CAB4B06409ECD1D79; PSTM=1541069619; BD_UPN=12314753; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; pgv_pvi=4045560832; BDUSS=o1SUlnZHJhen5DR0VXYlNPcXlpVDd2RDJaMFpFTzBUTWhzLXpDbzVkVE9Id2xjQUFBQUFBJCQAAAAAAAAAAAEAAADmUFVJTm90aGluZ-zhaXMAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAM6S4VvOkuFbb3; BDRCVFR[dKdo-B-qoyR]=9xWipS8B-FspA7EnHc1QhPEUf; BD_HOME=1; H_PS_PSSID=; WWW_ST=1541509866480',
    'Host': 'www.zhihu.com',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36',
}
r = requests.get('https://www.zhihu.com', headers=headers1)
print(r.text)

