
import json
import re
import os
import shutil
import urllib3
import chardet
from bs4 import BeautifulSoup

root = "http://www.osho.tw/cn/cnebook/"

def getHtml(url):
  http = urllib3.PoolManager()
  response = http.request('GET', url) 
  html = response.data
  det = chardet.detect(html)
  charset = det['encoding']
  html = html.decode(charset, 'ignore')
  result = html.encode('utf8', 'ignore')
  return result

def createOrUpdate(path, isUpdate = 'yes'):
  if (os.path.exists(path)):
    if (isUpdate != 'no'):
      shutil.rmtree(path)
      os.mkdir(path)
      print(f'{path} 更新成功!')
  else : 
    os.mkdir(path)
    print(f'{path} 创建成功!')

def getBookContent(url, index, name, dirPath):
  html = getHtml(root + url)
  print(root + url)
  book = BeautifulSoup(html, 'html.parser')
  bookContent = {}
  bookContent['title'] = []
  bookContent['content'] = []
  titleList = book.find_all('font')
  contentList = book.find_all('p')

  for t in titleList:
    titleItem = t.text.strip()
    if (titleItem):
      bookContent['title'].append(titleItem)

  for c in contentList:
    contentItem = c.text.strip()
    if (contentItem):
      bookContent['content'].append(contentItem)

  fw = open(f'{dirPath}/{index}.json', 'w', encoding='utf-8')
  json.dump(bookContent, fw, ensure_ascii=False)

def findAllFile():
  f = os.walk(r"./osho/")
  for path, dir_list, file_list in f:
    for dir_name in dir_list:
        print(os.path.join(path, dir_name))
        dirPath = os.path.join(path, dir_name)
        openPath = dirPath + '/index.json'
        with open(openPath, 'r') as bookCatalog:
          data = json.load(bookCatalog)
          for item in data['catalog']:
            url = item['chapUrl']
            name = item['chapName']
            index = item['id']
            getBookContent(url, index, name, dirPath)

findAllFile()