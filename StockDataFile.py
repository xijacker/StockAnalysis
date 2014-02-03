from stockconfig import *
from AllStocksData import StockData
import cPickle

class StockDataFile:
	def __init__(self, stockdata):
		if(dtype.lower() == 'min'):
			fileName = minStockDataFileName
		else:
			fileName = dailyStockDataFileName
		self.symbol = stockdata.symbol	
		self.fileName=fileName + '\\'+ stockdata.symbol #The file name and path on disk to store the stock Data
		self.headerfilename = self.fileName + '_Hdr'
	


	def Writestockdata2file(stockData):
		with open(self.fileName, 'a') as f:
			





