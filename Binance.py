from binance.client import Client
import datetime as dt
import time
import json
import pandas as pd

api = 'your api key'
secret = 'your secret key'

def myconverter(o):
    if isinstance(o, dt.datetime):
        return o.__str__()

client = Client(api, secret)

#Withdrawals - Start
withdrawals = client.get_withdraw_history()

for tr in withdrawals['withdrawList']:
    tr['applyTime'] = dt.datetime.fromtimestamp(int(tr['applyTime'])/1000)
    tr['successTime'] = dt.datetime.fromtimestamp(int(tr['successTime'])/1000)

with open('withdrawals.txt', 'w') as outfile:
        json.dump(withdrawals['withdrawList'], outfile, default=myconverter)    

data = pd.read_json("withdrawals.txt")
data.to_csv("Binance - withdrawals.csv")
#Withdrawals - End

#Deposits - Start
deposits = client.get_deposit_history()

for tr in deposits['depositList']:
    tr['insertTime'] = dt.datetime.fromtimestamp(int(tr['insertTime'])/1000)

with open('deposits.txt', 'w') as outfile:
        json.dump(deposits['depositList'], outfile, default=myconverter)    

data = pd.read_json("deposits.txt")
data.to_csv("Binance - deposits.csv")
#Deposits - End

trades = []
index = 0
recordcount = 500

instruments = client.get_exchange_info()

#Trades - Start
for instr in instruments['symbols']:       
    index = 0
    recordcount = 500  

    while(recordcount == 500):
        
        trade = client.get_my_trades(symbol=instr['symbol'], limit = 500, fromId = index)       
        
        if trade != [] and trade is not None:
            trades.extend(trade)            
           
            recordcount = len(trade)
            index = int(trade[recordcount - 1]['id']) + 1
        else:
            recordcount = 0

for tr in trades:
    tr['time'] = dt.datetime.fromtimestamp(int(tr['time'])/1000)

with open('trades.txt', 'w') as outfile:
        json.dump(trades, outfile, default=myconverter)    

data = pd.read_json("trades.txt")
data.to_csv("Binance - trades.csv")
#Trades - End

orders = []

#Orders - Start
for instr in instruments['symbols']:       
    index = 0
    recordcount = 500  

    while(recordcount == 500):
        
        order = client.get_all_orders(symbol=instr['symbol'], limit = 500, orderId = index)       
        
        if order != [] and order is not None:
            orders.extend(order)            
           
            recordcount = len(order)
            index = int(order[recordcount - 1]['orderId']) + 1
        else:
            recordcount = 0     

for tr in orders:
    tr['time'] = dt.datetime.fromtimestamp(int(tr['time'])/1000)

with open('orders.txt', 'w') as outfile:
        json.dump(orders, outfile, default=myconverter)    

data = pd.read_json("orders.txt")
data.to_csv("Binance - orders.csv")
#Orders - End

#Asset Balance - Start
assets = client.get_account()

with open('assets.txt', 'w') as outfile:
        json.dump(assets['balances'], outfile, default=myconverter)    

data = pd.read_json("assets.txt")
data.to_csv("Binance - assets.csv")
#Asset Balance - End