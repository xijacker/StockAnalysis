import time
import datetime
import MySQLdb as mdb
from stockconfig import *
from logging import Logger

class StockData(object):
    """ Stock Data """
    def __init__(self, type, stockSymbol, listPriceNames):

        self.listPriceNames = listPriceNames
        self.listPrices = []
        self.data = []  # List of SingleStockData
        self.type = type
        self.symbol = stockSymbol

    def isNewData(self, newData):
        if len(self.listPrices) == 0:
            return True
        isNew = False
        if(len(self.listPrices) > 0):
        #for d in self.listPrices:
            d = self.listPrices[len(self.listPrices)-1]
            for i in range(0, len(newData)-1):
                if(d[i] != newData[i]):
                    return True

        return False;           
    def addNewData(self, newdata):
        # Set the price of SingleStockData based on the download data from Yahoo Finance
        datanum = 0
        if(self.isNewData(newdata)):
            self.listPrices.append(newdata)
            datanum += 1
#       else:
        return datanum


class AllStocksData:
    """ All Data is a list of stock datas, each item is for a stock
     each item is an list of data for a stock, each item is for a trade information at specific time 
        """
    def __init__(self):
        self.AllData = []       # data for all the stocks which is a list of StockData
        self.stockNumber = 0    # number of stocks
        self.stockSymbols = []  # list of stock symbols
        self.setListPriceNames()# the list of data columns for all the stocks
        self.datanumber = 0     # Total number of data collected
        #self.addStockData(data)

    def setListPriceNames(self):
        """ Set the list based on the urlStr = url + stocks +'&f=sd1t1l1bahgopva5b6a2kjk3' in GetRealTimeStockData
        '&f=sd1t1l1bahgopva5b6k3a2kj'
        """
        self.listPriceNames = ['symbol', 'Trade Date Time', 'Last Trade', 'bid', 'ask', 'DayHigh', 'DayLow', 'Open', 'PreviousClose', 'Volume', 'AskSize', 'BidSize', 'AverageDailyVol', 'YearHigh', 'YearLow', 'LaskTradeSize']

    def addStockData(self, data):
        """" Add all the downloaded data to self.AllData  
        """
        for d in data:
            curStockData = d.split(',')
            # Add Single Stock Data
            self.addSingleStockData(curStockData)

    def addSingleStockData(self, d):
        """ Add a single stock data to all data AllData
         
        """
        if(len(d) < 10 or d[1]== '"N/A"' or d[2] == '"N/A"'): # no data
            return 

        newdata = []
        if(len(d) < len(self.listPriceNames)):
            return

        #print(d[0], 'd1', d[1], d[2], len(d))  
        newstock = False
        stockIdx = -1
        i = 0
        for s in self.stockSymbols:
            if(d[0] == s):
                stockIdx = i
            i = i+1

        try:    
            if(stockIdx == -1): # It is a new stock
                self.stockSymbols.append(d[0])
                newStockData = StockData('min', d[0], self.listPriceNames)
                self.AllData.append(newStockData)
                stockIdx = len(self.stockSymbols)-1
         
            newdata.append(d[0]) #add symbol
            hh = d[2].split(':')

            hh[0] = int(hh[0][1:len(hh[0])])
            if('p' in hh[1]):
                hh[0] = hh[0]+12
            hh[1] = int(hh[1][0:2])

            dt = d[1].split('/')
            #print(dt)
            dt = datetime.datetime(int(dt[2][0:len(dt[2])-1]), int(dt[0][1:len(dt[0])]), int(dt[1]), hh[0], hh[1])

            newdata.append(dt)  #date time
            
            for i in range(3, len(self.listPriceNames)+1):
                if(i < len(self.listPriceNames) and (i <= len(d))):
                    if('.' in d[i]):
                        newdata.append(float(d[i])) #float 
                    elif d[i].isnumeric():
                        newdata.append((d[i]))  # integer 
                    else:
                        newdata.append(-1)  # not a number
                else:
                    num = ''
                    while(i < len(d)):
                        num = num + d[i]
                        i += 1
                    if(num.isnumeric()):
                        newdata.append(num) #last trade price
                    else:
                        newdata.append(-1)

            self.datanumber += self.AllData[stockIdx].addNewData(newdata)
            #print(d)
        except:
            print("Error to generate data for", d)    
        #print(len(self.AllData), self.AllData[stockIdx].listPrices)


    def writeData2DB(self):
        """ Write Self.AllData to MySQL Database 
        """
        con = mdb.connect('localhost', 'root', 'ShuJuKu66', 'stocktrade')
        with con:
            cur = con.cursor()
            # ver = cur.fetchone()
            # print('dddddddddddddddddddddddddddddddddddddd', len(self.AllData))
            for s in self.AllData:
                for p  in s.listPrices:
                    #cur.execute("INSERT INTO minutestockdataz(symbol, dt, lastprice, bidprice, dayhigh, daylow, open, preclose, volume, asksize, bidsize, avergedailyvol, yearhigh, yearlow, lasttradevol) VALUES(self.AllData[i].listPrices(:))")
                    #cur.execute('''INSERT INTO minutestockdataz(symbol, dt, lastprice, bidprice, dayhigh, daylow, open, preclose, volume) VALUES (%s. %d, (s.listPrices[0],s.listPrices[1], s.listPrices[2],s.listPrices[3],s.listPrices[4],s.listPrices[5],s.listPrices[6],s.listPrices[7], s.listPrices[8]))
                    stockid = p[0]+p[1].isoformat()
                    #print(len(stockid), stockid, p[3])
                    #insertsql = "INSERT INTO minutetrade(tradeid, symbol, dt, lastprice, bidprice, dayhigh, daylow, open, preclose, volume, asksize, bidsize, averagedailyvol, yearhigh, yearlow, lasttradevol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s)", (stockid, p[0], p[1].isoformat(), p[2], p[3], p[4], p[5],p[6],p[7],p[8],p[9],p[10],p[11], p[12],p[13], p[14])
                    #cur.execute("INSERT INTO minutetrade(tradeid, symbol, dt, lastprice, bidprice, volume) VALUES (%s, %s, %s, %s, %s, %s)", (stockid, p[0], p[1].isoformat(), p[2], p[3], p[9]))
                    try:
                                                # print('eeeeeeeeeeeeeeeeeeeeeeeeeeee', len(s.listPrices), s.listPrices[0])
                        cur.execute("INSERT INTO minutetrade(tradeid, symbol, dt, lastprice, bidprice, askprice, dayhigh, daylow, open, preclose, volume, asksize, bidsize, averagedailyvol, yearhigh, yearlow, lasttradevol) VALUES (%s, %s, %s, %s, %s, %s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s)", (stockid, p[0], p[1].isoformat(), p[2], p[3], p[4], p[5],p[6],p[7],p[8],p[9],p[10],p[11], p[12],p[13], p[14], p[15]))
                        #cur.execute(insertsql)
                    except:
                        print( "Error when writing to MySQL: Integrity Error")

                    #print('Wrote:', p)
                s.listPrices[:] = []
            con.commit()
            self.datanumber = 0
        con.close()
