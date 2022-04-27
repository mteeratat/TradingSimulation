# https://python-binance.readthedocs.io/en/latest/
# https://algotrading101.com/learn/binance-python-api-guide/
# https://binance-docs.github.io/apidocs/spot/en/#general-info

import os
from binance.client import Client
import time
import pandas as pd

def buy(amount):
    wallet["USDT"] -= amount
    wallet["BTC"] += amount/float(btcusdt['price'])
    print("buy")
    return wallet

def sell(amount):
    wallet["BTC"] -= amount
    wallet["USDT"] += amount*float(btcusdt['price'])
    print("sell")
    return wallet

def emacross():
    if closeP['ema20'] > closeP['ema50']:
        while(True):
            if closeP['ema20'] < closeP['ema50']:
                print(sell(wallet["BTC"]))
    if closeP['ema20'] < closeP['ema50']:
        while(True):
            if closeP['ema20'] > closeP['ema50']:
                print(buy(wallet["BTC"]))


api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')

client = Client(api_key, api_secret)

# while(True):
#     time.sleep(10)
#     btcusdt = client.get_symbol_ticker(symbol='BTCUSDT')
    # print(btcusdt)

close = []
wallet = {"USDT": 1000, "BTC": 0}

candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, limit=50)
print(len(candles))
# print(candles)
for c in candles:
    close.append(c[4])

# print(close)

closeP = pd.DataFrame({'price': close})
closeP['ema20'] = closeP['price'].ewm(span=20, adjust=False).mean()
closeP['ema50'] = closeP['price'].ewm(span=50, adjust=False).mean()
print(closeP)
btcusdt = client.get_symbol_ticker(symbol='BTCUSDT')
print(btcusdt['price'])
# print(client.get_exchange_info())

# print(buy(10))
# print(sell(0.00005))
emacross()