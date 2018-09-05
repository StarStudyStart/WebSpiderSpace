#-*- coding:utf-8 -*-
import requests
upload_file = {'uploadFile':open('../123.png','rb')}
rq2 = requests.post("http://pythonscraping.com/pages/files/processing2.php",files=upload_file)
print(rq2.text)



