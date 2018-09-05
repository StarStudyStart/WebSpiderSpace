#HttpAuthTest.py
import requests
from requests.auth import AuthBase
from requests.auth import HTTPBasicAuth
auth = HTTPBasicAuth('Yabin','password')
rq = requests.post(url = 'http://pythonscraping.com/pages/auth/login.php',auth = auth)
print(rq.text)
