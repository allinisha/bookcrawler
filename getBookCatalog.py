
import json
import re
import os
import shutil
import urllib3
import chardet
from bs4 import BeautifulSoup

root = "http://www.osho.tw/cn/"

# 获取页面内容
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

# 获取单本书籍
def getSingleBook(url, bookName):
	dirPath = f"osho/{bookName}"
	createOrUpdate(dirPath)
	html = getHtml(root + url)
	soup = BeautifulSoup(html, 'html.parser')
	chapterList = soup.find_all('a')
	contentList = soup.find_all(['p', 'font'])
	resultJson = {}
	resultJson['catalog'] = []
	resultJson['content'] = []
	chapterindex = 1

	for a in chapterList:
		chapterName = a.text.replace('\n', '').replace('\t', '').strip()
		chapterUrl = a['href']
		chapter = {'id': chapterindex, 'chapName': chapterName, 'chapUrl': chapterUrl}
		resultJson['catalog'].append(chapter)
		chapterindex += 1

	for p in contentList:
		paragraph = p.text.strip()
		a = p.find_all('a')
		if (paragraph and len(a) == 0):
			resultJson['content'].append(paragraph)
		
	fw = open(f'osho/{bookName}/index.json', 'w', encoding='utf-8')
	json.dump(resultJson, fw, ensure_ascii=False)

with open('osho_library.json', 'r') as library:
	data = json.load(library)
	for item in data:
		url = item['url']
		bookName = str(item['id']) + '_' + item['title']
		getSingleBook(url, bookName)