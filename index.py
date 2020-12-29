import urllib3
import chardet
from bs4 import BeautifulSoup


http = urllib3.PoolManager()

url = 'http://www.osho.tw/cn/cnebook/book25_01.htm'
response = http.request('GET', url)
html = response.data
# soup = BeautifulSoup(response.data)
det = chardet.detect(html)
charset = det['encoding']
html = html.decode(charset, 'ignore')
result = html.encode('utf8', 'ignore')
print(result)