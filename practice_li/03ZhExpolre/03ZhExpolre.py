#coidng:uft-8
import requests
from pyquery import PyQuery as pq

def getHtmlText(url):
    """获取知乎返回数据"""
    headers = {
        "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36\
        (KHTML, like Gecko) Chrome/70.0.3538.67 Safari/537.36",
        "Cookie":r'_zap=e8cca798-805f-4fa8-bd29-ca71149c9819; d_c0="APCox8KBdg6PTpuAFB37pEeDPqUMxjFj8so=|1541251030"; capsion_ticket="2|1:0|10:1541251033|14:capsion_ticket|44:YjIwYzkzYzdjODM5NDViN2E1ZGExNmM2YjdhNTE2NDM=|02a4d5468b19ad367bcc7bc515aaf335e58d5499288b7f822efb7e1d263fe516"; z_c0="2|1:0|10:1541251060|4:z_c0|92:Mi4xNnU5VEFnQUFBQUFBNE9lMndvRjJEaVlBQUFCZ0FsVk45TzNLWEFDNjUybUxzek1icE01MDZJTmdKVUxrNDFGVDhB|7ec75f6f43e32f5ff754971598c0aead197ebf74c742d6fa294d21bc6f32b46f"; tst=r; q_c1=f8f2ca8cc0fa456cab7a8d1170add90d|1541251061000|1541251061000; __gads=ID=edbcb61c554a088b:T=1541256922:S=ALNI_MaU1Be_ZSEJQqlOubxpPiNZQaQMGQ; __utmv=51854390.100--|2=registration_date=20151126=1^3=entry_date=20151126=1; tgw_l7_route=1c2b7f9548c57cd7d5a535ac4812e20e; _xsrf=fd0c0787-ec6e-444d-8208-853ba2567b47; __utma=51854390.309667293.1541257233.1541257267.1541922448.3; __utmb=51854390.0.10.1541922448; __utmc=51854390; __utmz=51854390.1541922448.3.3.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/'
    }
    
    r = requests.get(url, headers=headers)
    return r.text
    
def handleData(html):
    """解析返回数据"""
    doc = pq(html)
    #question = doc("h2 .question_link a") #只能同时查找一个节点
    items = doc.find(".explore-tab .feed-item").items()
    print(items)
    for item in items:
        question = item.find("h2").text()
        author = item.find(".author-link-line a").text()
        answer = pq(item.find(".content").html()).text() # 文本中包含HTML标签 再次构建pyquery 将答案中文本内容内容全提取出来
        with open('explore.txt', 'a+', encoding="utf-8") as f:
            f.write("\n".join([question, author, answer]))
            f.write("\n\n{:=^50}\n".format('分割线'))
            
if __name__ == '__main__':
    html = getHtmlText("https://www.zhihu.com/explore")
    handleData(html)


