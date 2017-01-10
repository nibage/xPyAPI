import socket
import ssl
import json

class XTBSession:

    __streamSessionId = None

    def __init__(self, host, port, streamPort):
        '''Establishes connection with server)'''

        # replace host name with IP, this should fail connection attempt,
        # but it doesn't in Python 2.x
        host = socket.getaddrinfo(host, port)[0][4][0]

        # create socket and connect to server
        # server address is specified later in connect() method
        self.sock = socket.socket()
        self.sock.connect((host, port))

        # wrap socket to add SSL support
        self.sock = ssl.wrap_socket(self.sock,
          # flag that certificate from the other side of connection is required
          # and should be validated when wrapping 
          cert_reqs=ssl.CERT_REQUIRED,
          # file with root certificates
          ca_certs="/home/stepan/scripts/cacert.pem"
        )

        ################################################### STREAMING PORT  ################################################### 
        self.stream = socket.socket()
        self.stream.connect((host, streamPort))

        self.stream = ssl.wrap_socket(self.stream,
          # flag that certificate from the other side of connection is required
          # and should be validated when wrapping 
          cert_reqs=ssl.CERT_REQUIRED,
          # file with root certificates
          ca_certs="/home/stepan/scripts/cacert.pem"
        )

    #helper methods
    End=b'\n\n'

    def recv_end(self):
        total_data=[];data=''
        while True:
                data=self.sock.recv(8192)
                if self.End in data:
                    total_data.append(data[:data.find(self.End)])
                    break
                total_data.append(data)
                if len(total_data)>1:
                    #check if end_of_data was split
                    last_pair=total_data[-2]+total_data[-1]
                    if self.End in last_pair:
                        total_data[-2]=last_pair[:last_pair.find(self.End)]
                        total_data.pop()
                        break
        return b''.join(total_data)

    def __send_JSON(self, packet):
        '''sends packet to socket'''

        packet = json.dumps(packet, indent=4)
        self.sock.send(packet.encode("UTF-8"))
        print(packet + "\n")

        tmp = self.recv_end()
        tmp = str(tmp,'utf-8')
        tmp = json.loads(tmp)
        return tmp

    def openStream(self):
        '''open Streaming session'''
        pass
        
    def closeStream(self):
        '''close Streaming session'''
        pass

    def login(self, userId, password, appId="test", appName="test"):
        '''logins to the server'''
       
        tmp = self.__send_JSON({"command": "login",
                                  "arguments": {
                                    "userId": userId,
                                    "password": password,
                                    "appId": appId,
                                    "appName": appName
                                    }
                                  })
        self.__streamSessionId = str(tmp["streamSessionId"])
        return tmp

    def logout(self):
        '''logouts'''

        tmp = self.__send_JSON({"command": "logout"})
        return tmp

    # main communication commands

    def getAllSymbols(self):
        '''getAllSymbols'''

        tmp = self.__send_JSON({"command": "getAllSymbols"})
        return tmp

    def getCalendar(self):
        '''getCalendar'''

        tmp = self.__send_JSON({"command": "getCalendar"})
        return tmp

    def getChartLastRequest(self, period=5, start=1483816413833, symbol="EURUSD"):
        '''getChartLastRequest'''

        tmp = self.__send_JSON({
        "command": "getChartLastRequest",
        "arguments": {
                "info": {
                    "period": period,
                    "start": start,
                    "symbol": symbol
                }
            }
        })
        return tmp

    def getChartRangeRequest(self, start=1483982046000, end=1483982045000, period=5, symbol="EURUSD", ticks=0):
        '''getChartRangeRequest'''

        tmp = self.__send_JSON({
	    "command": "getChartRangeRequest",
	    "arguments": {
		    "info": {
	            "end": end,
	            "period": period,
	            "start": start,
	            "symbol": symbol,
	            "ticks": ticks
            }
	    }
    })
        return tmp

    def getCommissionDef(self, symbol="T.US", volume=1.0):
        '''getCommissionDef'''

        tmp = self.__send_JSON({
	    "command": "getCommissionDef",
	    "arguments": {
		    "symbol": symbol,
		    "volume": volume
	    }
    })
        return tmp

    def getCurrentUserData(self):
        '''getCurrentUserData'''

        tmp = self.__send_JSON({
	    "command": "getCurrentUserData"
    })
        return tmp

    def getIbsHistory(self, start=1394449010991, end=1395053810991):
        '''getIbsHistory'''

        tmp = self.__send_JSON({
	    "command": "getIbsHistory",
	    "arguments": {
		    "end": end,
		    "start": start
	    }
    })
        return tmp

    def getMarginLevel(self):
        '''getMarginLevel'''

        tmp = self.__send_JSON({
	    "command": "getMarginLevel"
    })
        return tmp

    def getMarginTrade(self, symbol="EURPLN", volume=1.0):
        '''getMarginTrade'''

        tmp = self.__send_JSON({
	    "command": "getMarginTrade",
	    "arguments": {
		    "symbol": symbol,
		    "volume": volume
	    }
    })
        return tmp

    def getNews(self, start=1275993488000, end=0):
        '''getNews'''

        tmp = self.__send_JSON({
	    "command": "getNews",
	    "arguments": {
		    "end": end,
		    "start": start
	    }
    })
        return tmp

    def getProfitCalculation(self, openPrice=1.2233, closePrice=1.3000, cmd=0, symbol="EURPLN", volume=1.0 ):
        '''getProfitCalculation'''

        tmp = self.__send_JSON({
	    "command": "getProfitCalculation",
	    "arguments": {
		    "closePrice": closePrice,
		    "cmd": 0,
		    "openPrice": openPrice,
		    "symbol": symbol,
		    "volume": volume
	    }
    })
        return tmp

    def getServerTime(self):
        '''getServerTime'''

        tmp = self.__send_JSON({
	    "command": "getServerTime"
    })
        return tmp

    def getStepRules(self):
        '''getStepRules'''

        tmp = self.__send_JSON({
	    "command": "getStepRules"
    })
        return tmp

    def getSymbol(self, symbol="EURPLN"):
        '''getSymbol'''

        tmp = self.__send_JSON({
	    "command": "getSymbol",
	    "arguments": {
		    "symbol": symbol
	    }
    })
        return tmp

#"symbols": ["EURPLN", "AGO.PL", ...],

    def getTickPrices(self,  symbols, level=0, timestamp=1262944112000):
        '''getTickPrices'''

        tmp = self.__send_JSON({
	    "command": "getTickPrices",
	    "arguments": {
		    "level": level,
		    "symbols": symbols,
		    "timestamp": timestamp
	    }
    })
        return tmp

    def getTradeRecords(self, orders):
        '''getTradeRecords'''

        tmp = self.__send_JSON({
	    "command": "getTradeRecords",
	    "arguments": {
		    "orders": orders # "orders": [7489839, 7489841, ...]
	    }
    })
        return tmp

    def getTrades(self, openedOnly=True):
        '''getTrades'''

        tmp = self.__send_JSON({
	    "command": "getTrades",
	    "arguments": {
		    "openedOnly": openedOnly
	    }
    })
        return tmp

    def getTradesHistory(self, start=1275993488000 ,end=0):
        '''getTradesHistory'''

        tmp = self.__send_JSON({
	    "command": "getTradesHistory",
	    "arguments": {
		    "end": end,
		    "start": start
	    }
    })
        return tmp

    def getTradingHours(self, symbols): #	    "symbols": ["EURPLN", "AGO.PL", ...]
        '''getTradingHours'''

        tmp = self.__send_JSON({
	    "command": "getTradingHours",
	    "arguments": {
		    "symbols": symbols
	    }
    })
        return tmp

    def getVersion(self):
        '''getVersion'''

        tmp = self.__send_JSON({
	    "command": "getVersion"
    })
        return tmp

    def ping(self):
        '''ping'''

        tmp = self.__send_JSON({
	    "command": "ping",
        "streamSessionId": self.__streamSessionId
    })
        return tmp

    def tradeTransaction(self, cmd, comment="Some text", expiration=0, order=0, price=1.12, sl=0.0, symbol="EURUSD", tp=0.0, transtype=0, volume=5.0 ):
        '''tradeTransaction'''

        tmp = self.__send_JSON({
        "command": "tradeTransaction",
	    "arguments": {
		    "tradeTransInfo": {
	            "cmd": cmd,
	            "customComment": comment,
	            "expiration": expiration,
	            "order": order,
	            "price": price,
	            "sl": sl,
	            "symbol": symbol,
	            "tp": tp,
	            "type": transtype,
	            "volume": volume
            }
	    }
    })
        return tmp

    def tradeTransactionStatus(self, oder):
        '''tradeTransactionStatus'''

        tmp = self.__send_JSON({
	    "command": "tradeTransactionStatus",
	    "arguments": {
		    "order": order
	    }
    })
        return tmp

 ####################################################################
    #Streaming commands - must send data to streaming server!

 ####################################################################

    def getBalance(self):
        '''getBalance'''
        
        packet = json.dumps({
        "command": "getBalance",
	    "streamSessionId": self.__streamSessionId}, indent=4)
        self.stream.send(packet.encode("UTF-8"))

        tmp = self.stream.recv(8000)
        tmp = str(tmp,'utf-8')

        return tmp

    def getCandles(self):
        '''getCandles'''

        packet = json.dumps({
        "command": "getCandles",
    	"streamSessionId": self.__streamSessionId,
	    "symbol": "EURUSD",
    	"onlyComplete": 1,
	    "period": 5

    }, indent=4)
        self.stream.send(packet.encode("UTF-8"))

        tmp = self.stream.recv(8000)
        tmp = str(tmp,'utf-8')

        return tmp

    def getKeepAlive(self):
        '''getKeepAlive'''

        packet = json.dumps({
	"command": "getKeepAlive",
	"streamSessionId": self.__streamSessionId,
    }, indent=4)
        self.stream.send(packet.encode("UTF-8"))

        tmp = self.stream.recv(8000)
        tmp = str(tmp,'utf-8')

        return tmp

    def getSNews(self):
        '''getKeepAlive'''

        packet = json.dumps({
	"command": "getNews",
	"streamSessionId": "8469308861804289383"
    }, indent=4)
        self.stream.send(packet.encode("UTF-8"))

        tmp = self.stream.recv(8000)
        tmp = str(tmp,'utf-8')

        return tmp


    def getProfits(self):
        '''getProfits'''
        packet = json.dumps({
	    "command": "getProfits",
	    "streamSessionId": self.__streamSessionId
    }, indent=4)
        self.stream.send(packet.encode("UTF-8"))

        tmp = self.stream.recv(8000)
        tmp = str(tmp,'utf-8')

        return tmp

    def getSTickPrices(self, symbol, minArrivalTime=5000, maxLevel=2):
        '''getSTickPrices'''

        packet = json.dumps({
	    "command": "getTickPrices",
	    "streamSessionId": self.__streamSessionId,
	    "symbol": "EURUSD",
	    "minArrivalTime": 5000,
	    "maxLevel": 2
        }, indent=4)
        self.stream.send(packet.encode("UTF-8"))

        tmp = self.stream.recv(8000)
        tmp = str(tmp,'utf-8')
        return tmp

    def getSTrades(self, symbol, minArrivalTime=5, maxLevel=2):
        '''getSTickPrices'''

        packet = json.dumps({
	    "command": "getTrades",
	    "streamSessionId": self.__streamSessionId
        }, indent=4)
        self.stream.send(packet.encode("UTF-8"))

        tmp = self.stream.recv(8000)
        tmp = str(tmp,'utf-8')
        return tmp


    def getTradeStatus(self):
        '''getTradeStatus'''

        packet = json.dumps({
	    "command": "getTradeStatus",
	    "streamSessionId": self.__streamSessionId
        }, indent=4)
        self.stream.send(packet.encode("UTF-8"))

        tmp = self.stream.recv(8000)
        tmp = str(tmp,'utf-8')

        return tmp

    def getVersion(self):
        '''getVersion'''

        tmp = self.__send_JSON({
	"command": "getVersion"
    })
        return tmp




