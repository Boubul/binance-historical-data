# binance-historical-data
This python code will help you to extract data from Binance Cryptocurrency and export it to csv file.

First, use the below code to install binance library,

**`pip install binance`**

then,

**`pip install pandas`**

Below are the list of reports you can extract from Binance,

- Withdraw history
- Deposits history
- Trades history
- Orders history
- Asset balance

## Explanation

### Connect to Client

**`client = Client(api, secret)`**

### Withdraw history

```
withdrawals = client.get_withdraw_history()

for tr in withdrawals['withdrawList']:
    tr['applyTime'] = dt.datetime.fromtimestamp(int(tr['applyTime'])/1000)
    tr['successTime'] = dt.datetime.fromtimestamp(int(tr['successTime'])/1000)

with open('withdrawals.txt', 'w') as outfile:
        json.dump(withdrawals['withdrawList'], outfile, default=myconverter)    

data = pd.read_json("withdrawals.txt")
data.to_csv("Binance - withdrawals.csv")
```

### Deposits history

```
deposits = client.get_deposit_history()

for tr in deposits['depositList']:
    tr['insertTime'] = dt.datetime.fromtimestamp(int(tr['insertTime'])/1000)

with open('deposits.txt', 'w') as outfile:
        json.dump(deposits['depositList'], outfile, default=myconverter)    

data = pd.read_json("deposits.txt")
data.to_csv("Binance - deposits.csv")
```

### Trade history

```
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
```

### Order history

```
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
```

### Asset balance

```
assets = client.get_account()

with open('assets.txt', 'w') as outfile:
        json.dump(assets['balances'], outfile, default=myconverter)    

data = pd.read_json("assets.txt")
data.to_csv("Binance - assets.csv")
```
