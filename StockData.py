minStockDataFileName = 'Data\\StockDataMin'	# Stock Data by Minutes
dailyStockDataFileName = 'Data\\StockDataDaily'	# Daily Stock Data

class SingleStockData(object):
	stockName = ''		# The stock name
	listPriceNames = [] # the prices names related the listPrices
	listPrices = []

	def __init__(self, data):
		addStockData(data)


	def addStockData(data):
		stockName  


class StockData(object):
	fileName = ''  #The file name and path on disk to store the stock Data
	dataNumber = 0	#The number of data included in the StockData
	data = []	# List of SingleStockData
	listPriceNames = []
	listPrices = []
	def setListPriceNames(self):
		# Set the list based on the urlStr = url + stocks +'&f=sd1t1l1bahgopva5b6k3a2kj' in GetRealTimeStockData
		#'&f=sd1t1l1bahgopva5b6k3a2kj'
		self.listPriceNames = ['symbol', 'Date', 'Trade Time', 'Last Trade', 'bid', 'ask', 'DayHigh', 'DayLow', 'Open', 'PreviousClose', 'Volume', 'AskSize', 'BidSize', 'LaskTradeSize', 'AverageDailyVol', 'YearHigh', 'YearLow']
	
	def __init__(self, type):

		if(type == 'Min'):
			fileName = minStockDataFileName
		else:
			fileName = dailyStockDataFileName

		setListPriceNames(self)

	def setPrice(self, data):
		# Set the price of SingleStockData based on the download data from Yahoo Finance
		self.listPrices = []
		

class AllStocksData(object):
	AllData = []
	stockNumber = 0
	stockSymbols = []

	def __init(self):
		self.stockNumber = 0
		self.stockSymbols = []

	def addStockData(data):
		for d in data:
			print(d, len(d))



