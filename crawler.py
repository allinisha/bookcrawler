#coding:utf-8

# 引入模块
import json
import shutil
import os
import requests
from bs4 import BeautifulSoup

home = "http://www.osho.tw/cn/cn_004.htm"
root = "http://www.osho.tw/cn/"
# http://www.osho.tw/cn/cnebook/book18_01.htm
# url = "http://www.osho.tw/cn/cnebook/book18_01.htm"

def createOrUpdate(path, isUpdate = 'yes'):
	if (os.path.exists(path)):
		if (isUpdate != 'no'):
			shutil.rmtree(path)
			os.mkdir(path)
			print(f'{path} 更新成功!')
	else : 
		os.mkdir(path)
		print(f'{path} 创建成功!')

		
# 获取所有书籍
def getAllBooks(url):
	createOrUpdate('奥修', 'no')
	data = requests.get(url)
	soup = BeautifulSoup(data.text, 'lxml')
	bookList = soup.select('div table table table table tr')
	bookIndex = 0
	library = []

	for bookRow in bookList:
		bookRowItem = bookRow.select('td')
		for book in bookRowItem:
			bookIndex += 1 
			if (len(book.select('a')) != 0):
				href = book.select('a')[0].get('href')
				bookName = book.select('font')[0].text.replace(u'\xa0', u'').encode('ISO-8859-1').decode('gb18030', 'ignore').strip()
				library.append({'bookName': bookName, 'id': bookIndex})
				getSingleBook(href, bookName)
			break
	fw = open(f'osho_library.json', 'w', encoding='utf-8')
	json.dump(library, fw, ensure_ascii=False)		
			
# 获取单本书籍
def getSingleBook(url, bookName):
	dirPath = f"奥修/{bookName}"
	createOrUpdate(dirPath)
	data = requests.get(root + url)
	soup = BeautifulSoup(data.text, 'lxml')
	chapterList = soup.select('a[href]')
	resultJson = {}
	resultJson['catalog'] =[]

	# 原序
	defaultPreFace = soup.select('body>p[algin="center"]')
	if (len(defaultPreFace) > 0):
		defaultPreFace = defaultPreFace[0]
		resultJson['defaultPreFace'] = defaultPreFace

	# 译文序
	TranslationPreFace = []
	if (len(TranslationPreFace) > 0):
			TranslationPreFace = TranslationPreFace[0]
			resultJson['TranslationPreFace'] = TranslationPreFace
		
	# 目录
	for index in range(len(chapterList)):
		chapter = chapterList[index]
		chapterIndex = index+1
		chapterUrl = chapter.get('href')
		chapterName = chapter.text.encode('ISO-8859-1').decode('gb18030', 'ignore').strip()
		if (len(chapterUrl) > 0):
			catalogItem = {'chapterName': chapterName, 'chapterIndex': chapterIndex, 'chapterUrl': root+chapterUrl}
			resultJson['catalog'].append(catalogItem)
			getSingleChapter(chapterUrl, chapterName, chapterIndex, bookName)
			print(bookName, '--', chapterName)
		
	

# 获取书籍单章节
def getSingleChapter(url, name, index, bookName):
	data = requests.get(f'{root}cnebook/{url}')
	soup = BeautifulSoup(data.text, 'lxml')
	# bookName = soup.select('div table table tr td b')[0].text.encode('ISO-8859-1').decode('gb18030').strip()

	
	# chapterName = soup.select('div table table tr:nth-of-type(2) td p')[0].text.encode('ISO-8859-1').decode('gb18030').strip()
	sections = soup.select('body>p[style="line-height: 150%"]')
	chapterJson = {}
	chapterJson['chapterName'] = name
	chapterJson['contentList'] = []
	
	for section in sections:
		# \xa0是unicode编码的空字符，用gb18030编码处理会报错，如果用ignore又会出现乱码，把这东西替换掉就欧克了
		section = section.text.replace(u'\xa0', u'').replace(u'刹', u'É²').encode('ISO-8859-1').decode('gb18030', 'ignore')
		print(section)

		
		chapterJson['contentList'].append(section) 

	fw = open(f'奥修/{bookName}/{index}.json', 'w', encoding='utf-8')
	json.dump(chapterJson, fw, ensure_ascii=False)

getAllBooks(home)

