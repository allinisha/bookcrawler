import requests
from bs4 import BeautifulSoup

# str4 = 'É²'
# # print(len(str2))
# encodeTar = str4.encode('gb18030').decode('ISO-8859-1')
# encodeTar = str4.encode('gb18030').decode('ISO-8859-1')
# encodeTar2 = str4.encode('ISO-8859-1').decode('gb18030')
# # replaceStr = str2.replace(u'\xa0', u'')
# # print(encodeTar2, type(encodeTar))
# print(str4, type(str4))




# # 章节报错测试
# def getSingleChapter(url):
# 	data = requests.get(url)
# 	soup = BeautifulSoup(data.text, 'lxml')
# 	# bookName = soup.select('div table table tr td b')[0].text.encode('ISO-8859-1').decode('gb18030').strip()

# 	# chapterName = soup.select('div table table tr:nth-of-type(2) td p')[0].text.encode('ISO-8859-1').decode('gb18030').strip()
# 	sections = soup.select('body>p[style="line-height: 150%"]')
	
# 	for section in sections:
# 		# \xa0是unicode编码的空字符，用gb18030编码处理会报错，如果用ignore又会出现乱码，把这东西替换掉就欧克了
# 		# section = section.text.replace(u'\xa0', u'')
# 		# section = section.text.replace(u'\xa0', u'').encode('ISO-8859-1')
# 		section = section.text.replace(u'\xa0', u'').replace(u'刹', u'É²').encode('ISO-8859-1').decode('gb18030', 'ignore')
# 		print(section)

# getSingleChapter('http://www.osho.tw/cn/cnebook/book18_02.htm')