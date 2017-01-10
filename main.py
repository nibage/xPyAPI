
from XTBSession import XTBSession
import json
import time


connection_data = ['xapib.x-station.eu', 5124, 5125]

login_data = [10086262, "CASIOPEA"]

#tradeTransaction = [cmd["BUY"], "some text", 1462006335000, 0, 0, 1.2, 0.0, symbol[0], 0.0, transType["open"], 5.0  ]

transType = {
"OPEN"	    :0,
"PENDING"	:1,
"CLOSE"	    :2,
"MODIFY"	:3,
"DELETE"	:4,
}

period = {
'PERIOD_M1'	:1,
'PERIOD_M5'	:5,	
'PERIOD_M15'	:15,
'PERIOD_M30'	:30,
'PERIOD_H1'	:60,
'PERIOD_H4'	:240,	
'PERIOD_D1'	:1440,	
'PERIOD_W1'	:10080,
'PERIOD_MN1'	:43200,
}

cmd = {
'BUY'        :0,
'SELL'       :1,
'BUY_LIMIT'  :2,
'SELL_LIMIT' :3,
'BUY_STOP'   :4,
'SELL_STOP'  :5,
'BALANCE'    :6,
'CREDIT '    :7,
}

errorCodes = {"Error code" : "Error description",
    "BE001" :	"Invalid price",
    "BE002" :	"Invalid StopLoss or TakeProfit",
    "BE003" :	"Invalid volume",
    "BE004" :	"Login disabled",
    "BE005" :	"userPasswordCheck: Invalid login or password.",
    "BE006" :	"Market for instrument is closed",
    "BE007" :   "Mismatched parameters",
    "BE008" :	"Modification is denied",
    "BE009" :	"Not enough money on account to perform trade",
    "BE010" :	"Off quotes",
    "BE011" :	"Opposite positions prohibited",
    "BE012" :	"Short positions prohibited",
    "BE013" :	"Price has changed",
    "BE014" :	"Request too frequent",
    "BE016" :   "BE017	Too many trade requests",
    "BE018" :	"Trading on instrument disabled",
    "BE019" :	"Trading timeout",
    "BE020" :	"Other error", #BE020-BE037
    "BE037" :	"Other error",
    "BE099" :	"Other error",
    "BE094" :	"Symbol does not exist for given account",
    "BE095" :	"Account cannot trade on given symbol",
    "BE096" :	"Pending order cannot be closed. Pending order must be deleted",
    "BE097" :	"Cannot close already closed order",
    "BE098" :	"No such transaction",
    "BE101" :	"Unknown instrument symbol",
    "BE102" :	"Unknown transaction type",
    "BE103" :	"User is not logged",
    "BE104" :	"Method does not exist",
    "BE105" :	"Incorrect period given",
    "BE106" :	"Missing data",
    "BE110" :	"Incorrect command format",
    "BE115" :   "Symbol does not exist",
    "BE116" :	"Symbol does not exist",
    "BE117" :	"Invalid token",
    "BE118" :	"User already logged",
    "BE200" :	"Session timed out.",
    "EX000" :	"Invalid parameters",
    "EX001" :   "Internal error, in case of such error, please contact support",
    "EX002" :   "Internal error, in case of such error, please contact support",
    "SExxx" :   "Internal error, in case of such error, please contact support",
    "BE000" :   "Internal error, in case of such error, please contact support",
    "EX003" :	"Internal error, request timed out",
    "EX004" :	"Login credentials are incorrect or this login is not allowed to use an application with this appId",
    "EX005" :	"Internal error, system overloaded",
    "EX006" :	"No access",
    "EX007" :	"userPasswordCheck: Invalid login or password. This login/password is disabled for 10 minutes (the specific login and password pair is blocked after an unsuccessful login attempt).",
    "EX008" :	"You have reached the connection limit. For details see the Connection validation section.",
    "EX009" :	"Data limit potentially exceeded. Please narrow your request range. The potential data size is calculated by: (end_time - start_time) / interval. The limit is 50 000 candles",
    "EX010" :	"Your login is on the black list, perhaps due to previous misuse. For details please contact support.",
    "EX011" :	"You are not allowed to execute this command. For details please contact support.",
        }

timeInt = {
"hour" :3600000, 
"day"  :86400000, 
"week" :604800000, 
"month":2629743000, 
"year" :31556926000,
}

symbol = []

session = XTBSession(*connection_data)

session.login(*login_data)

command = session.getChartLastRequest(5, 1000*round(time.time())-timeInt["hour"]
, "EURUSD")

print(command["returnData"]["rateInfos"])

tmp = command["returnData"]["rateInfos"]

print("\n\n")

for i in tmp:
    print(i)
    


#getTradingHours(["EURUSD"])

#getTradeStatus() trvá moc dlouho

#getSTrades("EURUSD") nic nevrací

#getSTickPrices("EURUSD")

#getProfits() TRVÁ MOC DLOUHO!

#getKeepAlive()

#getProfits()

#getBalanc()

#getCandles()

#getBalance()

# session.getServerTime()

#getProfitCalculation()

# session.getNews()

# session.getChartLastRequest()

#session.getTradesHistory(round(time.time()-timeInt["hour"]), 0)
#session.getTrades()
#session.tradeTransaction(*[0, "Moje poznamka", 0, 0, 1.4, 0, "EURUSD", 0, transType["OPEN"], 5.0])

2
#session.getChartRangeRequest(round(time.time()),round(time.time()-timeInt["hour"]), 5, "EURUSD", 0)

session.logout()


