""" The constant data and configuration for stock analysis"""

minStockDataFileName = 'Data\\StockDataMin'	# Stock Data by Minutes
dailyStockDataFileName = 'Data\\StockDataDaily'	# Daily Stock Data

starthh = 9	# The stock trade start time in hour
startmm = 45 # The stock trade start time at minute
endhh = 16	# The stock trade start time in hour
endmm = 15 # The stock trade start time at minute
WeekInSec = 7 * 24 * 60 * 60 #seconds for a week
DayInSec = 24 * 60 * 60 # seconds for a day
HourInSec = 60 * 60 # seconds for one hour
MinInSec = 60 # the seconds for each minute
MaxBuffDataNum = 3  # the average received data number start write data to mySQL
MaxSleepTime = 30 *60 # The maximum sleeping time in seconds

stockDataFreq = 60.0 # seconds for reload stock data

stockStartTime = (starthh*60 + startmm) * 60 	# the stock market start time in seconds from 0am
stockEndTime = (endhh*60 + endmm) * 60 	#  the stock market stop time in seconds from 0am
weekEndTime = 4 * DayInSec + stockEndTime # seconds till the weekend from monday 0am
