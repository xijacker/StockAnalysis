from AllStocksData import AllStocksData
from timeit import default_timer
import time
from stockconfig import *



#import sqlite3 as mdb #SQLite3
import MySQLdb as mdb #MySQL

#url = "http://web.tmxmoney.com/quote.php?qm_symbol="
url = 'http://finance.yahoo.com/d/quotes.csv?s=' 
stockFileName = 'E.txt'
#stockName = "HOD"
#import urllib.request  #python 3.3
import urllib2                  #pthon 2.7
#from google.appengine.api import urlfetch

import sys

def GetRealTimeStockData(stockNames):
    #urlName = url +  stockName
    stocks = ''
    #print(stockNames)
    for s in stockNames:
        stocks = stocks + s.rstrip() + '+'
    
    if(len(s) > 0):
        stocks = stocks[:len(stocks)-1]

    urlStr = url + stocks +'&f=sd1t1l1bahgopva5b6a2kjk3' 
    #print(urlStr)
    d =[]
    try:
        req = urllib2.Request(urlStr)
        response = urllib2.urlopen(req)
        d = response.read()
    except:
        print('Read data from url error!')
    data = ''
    for row in d:
        data = data + row.decode("utf-8")
    data = data.split("\r\n")

    return data

'''
def AddData2DataBaseSQLite(data):
    try:
        con = mdb.connect('localhost', 'root', 'ShuJuKu66', 'stocktrade')
        #con = mdb.connect('localhost', 'david', 'myShuJuKu')
        cur = con.cursor()
        cur.execute('select SQLITE_VERSION()')
        d = cur.fetchone()
        print("Sqlite version: %s" %d)
#               cur.execute("""use stocktrade""")
#               con.commit()
        print("Database connection : %s " %con)
        print("Cursor : %s " %cur)
        cur.execute("""CREATE TABLE people
             (id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE NOT NULL,
             name TEXT NOT NULL,
             address TEXT,
             age  INTEGER)""" )     # AUTOINCREMENT is correct for sqlite3
        con.commit()                 # Does nothing for a database without
                        # Transactions.
        
        con.close()                  # Close the connection to the database             
    except ValueError:
        print ('Cannot start MySQL')
        sys.exit()
    finally:
        if con:
            con.close() 
'''

def AddData2DataBase(data):
    try:
        con = mdb.connect('localhost', 'root', 'ShuJuKu66', 'stocktrade')
        #con = mdb.connect('localhost', 'david', 'myShuJuKu')
        cur = con.cursor()
        cur.execute("SELECT VERSION()")

        ver = cur.fetchone()
        
        with con:
            
            cur = con.cursor()
        #print "Database version : %s " % ver
        
    except mdb.Error, e:
      
        print "Error %d: %s" % (e.args[0],e.args[1])
        sys.exit(1)
        
    finally:    
        
        if con:    
            con.close()


def RealStockDataCollection():
    with open(stockFileName, 'r')  as f:
        stockNames = f.read()
    f.close()
    
    StockNames = stockNames.split(',')
    data = GetRealTimeStockData(StockNames)
    AddData2DataBase(data)

    #print(data)
    return(data)


allStocks = AllStocksData()

curTime = time.localtime(time.time())
print('current time: ', curTime)

data = []
#AddData2DataBase(data)
i = 0
while(True):
    curTime = time.localtime(time.time())
    curDTimeInSec = curTime.tm_hour*HourInSec + curTime.tm_min * 60 + curTime.tm_sec # The time in second from today's morning (00:00am today) 
    curWTimeInSec = curTime.tm_wday * DayInSec + curDTimeInSec      # The time in second from the week start (Monday, 00:00am) 
    sleeptime = 0
    
    if (curWTimeInSec > weekEndTime):
        sleeptime = 6 * DayInSec + stockStartTime - curWTimeInSec;              #sleep to next monday morning
    elif(curDTimeInSec < stockStartTime):
        sleeptime = stockStartTime - curDTimeInSec              # To start time next day
    elif(curDTimeInSec > stockEndTime):
        sleeptime =  DayInSec + stockStartTime - curDTimeInSec  # To start time today 
    else:
        sleeptime = 0 
    sleeptime = min(sleeptime, MaxSleepTime)
    sleeptime = 0 # force it run for DEBUG only
    if(sleeptime == 0):
        start = default_timer()
        data = RealStockDataCollection()
        allStocks.addStockData(data)
        sleeptime = stockDataFreq - default_timer() + start
    print('Data collected: ', allStocks.datanumber)
    #if(allStocks.datanumber > MaxBuffDataNum* len(allStocks.stockSymbols)) or (allStocks.datanumber > 0 and sleeptime > 0):
    if(allStocks.datanumber > MaxBuffDataNum* len(allStocks.stockSymbols) or (sleeptime > MaxBuffDataNum * stockDataFreq)):
        # Write Data to file
        data = RealStockDataCollection()
        allStocks.addStockData(data)
        print('Writing to database at ....', curTime, allStocks.datanumber)
        allStocks.writeData2DB()

    if(sleeptime > 0):
        print('The system will sleep:', sleeptime, 'seconds ...', curWTimeInSec, weekEndTime, curDTimeInSec, stockStartTime, stockEndTime)
        time.sleep(sleeptime)


