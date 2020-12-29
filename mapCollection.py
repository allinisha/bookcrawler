#coding:utf-8

import json
import re
import urllib3
import chardet
from bs4 import BeautifulSoup

home = "http://www.osho.tw/cn/cn_004.htm"
root = "http://www.osho.tw/cn/"

http = urllib3.PoolManager()
response = http.request('GET', home) 
html = response.data
det = chardet.detect(html)
charset = det['encoding']
html = html.decode(charset, 'ignore')
result = html.encode('utf8', 'ignore')

books = []

# 获取所有图书url
def getAllBook():
  booksindex = 1
  soup = BeautifulSoup(html, 'html.parser')
  aList = soup.find_all('a')
  for a in aList:
    bookName = a.text.replace('\n', '').replace('\t', '').replace(' ', '')
    href = a['href']
    if (bookName):
      books.append({'id': booksindex, 'title': bookName, 'url': href, 'valid': 'false'})
      booksindex += 1
    
getAllBook()
fw = open('osho_library.json', 'w', encoding='utf-8')
json.dump(books, fw, ensure_ascii=False)

# 获取每本图书所有章节url
# 生成地图文本
# 根据标志决定是否拉取书籍
# 拉取每本书籍

