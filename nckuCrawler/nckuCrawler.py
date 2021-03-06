import re
import sys
import json
import requests
from time import sleep
from bs4 import BeautifulSoup  

class NckuCrawler(object):
	
	def __init__(self):
		self.l =[]
		self.start = int(sys.argv[1])
		self.end = int(sys.argv[2])

	#自定清除格式1
	def format(self,unformat):
		try:
			format = unformat.encode('raw_unicode_escape').decode('utf-8').replace(' ', '').replace('\n', '').replace('\t', '') 
			return format
		except:
			pass

	#自定清除格式1	
	def format2(self,unformat):
		try:
			format = unformat.encode('raw_unicode_escape').decode('utf-8').replace('\n', '').replace('\t', '') 
			return format
		except:
			pass

	def crawler(self,start,end):
		for key in range(start,end):
			print( 'index is '+str(key) )
			url = "http://web.ncku.edu.tw/files/501-1000-1048-"+str(key)+".php"
			resp = requests.get(url=url)
			soup = BeautifulSoup(resp.text)
			for tag in soup.find_all("tr",class_=re.compile("row_0")):	
				date = self.format( tag.contents[1].string )
				title = self.format2( tag.find("a") )
				organization = self.format( tag.contents[5].string )
				dic = {"日期":date,"標題":title,"公告單位":organization} 
				print(dic)
				self.l.append(dic)
				sleep(0.1)
			sleep(3)

	def storage(self,l):
		json_data = json.dumps(l,ensure_ascii=False)
		with open('ncku.json', 'w') as f:
			f.write(json_data)

	def run(self):
		self.crawler(self.start,self.end)
		self.storage(self.l)

#主函數
def main() :
    nckuCrawler = NckuCrawler()
    nckuCrawler.run()

if __name__ == '__main__' :
    main()
