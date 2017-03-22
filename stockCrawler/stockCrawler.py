
import sys
import mechanize
import pandas as pd
from bs4 import BeautifulSoup  

class StockCrawler(object):
	
	def __init__(self):
		self.l =[]
		self.unformat_l =[]
		self.year = sys.argv[1]
		self.month = sys.argv[2]

	def format(self):
		temp = range(len(self.unformat_l))
		for x in temp[1::2]:
			self.l.append(self.unformat_l[x])

	def crawler(self,year,month):
		br = mechanize.Browser()
		res = br.open("http://www.twse.com.tw/ch/trading/exchange/STOCK_DAY/genpage/Report"+str(year)+str(month)+"/"+str(year)+str(month)+"_F3_1_8_6214.php?STK_NO=6214&myear="+str(year)+"&mmon="+str(month))
		soup = BeautifulSoup(res)
		res = soup.find("table", class_="board_trad")
		for tag in res.find_all(class_="basic2"):
			l=[]
			for tag2 in tag.find_all('td'):
				l.append(tag2.string)
			self.unformat_l.append(l)

	def storage(self):
		df = pd.DataFrame(self.l,columns=['Date','Trade Volume','Trade Value','Opening Price','Highest Price','Lowest Price','Closing Price','Change','Transaction'])
		df = df.set_index('Date')
		with open('data.csv', 'w') as f:
		    df.to_csv(f)

	def run(self):
		self.crawler( self.year,self.month )
		self.format()
		self.storage()

def main() :
	try:
	    stockCrawler = StockCrawler()
	    stockCrawler.run()
	    print('creat data.csv succuess')
	except:
		print('''please format year and month  e.x 2014 07 if don't work the website have no data''')
		
if __name__ == '__main__' :
    main()


