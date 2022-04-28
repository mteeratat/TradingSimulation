# https://python-binance.readthedocs.io/en/latest/
# https://algotrading101.com/learn/binance-python-api-guide/
# https://binance-docs.github.io/apidocs/spot/en/#general-info

import os
from binance.client import Client
import time
import pandas as pd

def data():
    global close, closeP, btcusdt
    candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, limit=50)
    print(len(candles))
    for c in candles:
        close.append(c[4])
    closeP = pd.DataFrame({'price': close})
    closeP['ema20'] = closeP['price'].ewm(span=20, adjust=False).mean()
    closeP['ema50'] = closeP['price'].ewm(span=50, adjust=False).mean()
    print(closeP.iloc[49])
    btcusdt = client.get_symbol_ticker(symbol='BTCUSDT')

def buy(amount, wallet):
    wallet["USDT"] -= amount
    wallet["BTC"] += amount/float(btcusdt['price'])
    print("buy")
    return wallet

def sell(amount, wallet):
    wallet["BTC"] -= amount
    wallet["USDT"] += amount*float(btcusdt['price'])
    print("sell")
    return wallet

def emacross():
    while(True):
        while(closeP['ema20'].iloc[49] > closeP['ema50'].iloc[49] and float(btcusdt['price']) > closeP['ema20'].iloc[49]):
            print("s")
            data()
            if closeP['ema20'].iloc[49] < closeP['ema50'].iloc[49]:
                print("sell")
                print(sell(0.01, walletEMA))
                break
            time.sleep(10)
        while(closeP['ema20'].iloc[49] < closeP['ema50'].iloc[49] and float(btcusdt['price']) < closeP['ema20'].iloc[49]):
            print("b")
            data()
            if closeP['ema20'].iloc[49] > closeP['ema50'].iloc[49]:
                print("buy")
                print(buy(10, walletEMA))
                break
            time.sleep(10)
            # print(buy(10, walletEMA))

# def befema():

api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')

client = Client(api_key, api_secret)

# while(True):
#     time.sleep(10)
#     btcusdt = client.get_symbol_ticker(symbol='BTCUSDT')
    # print(btcusdt)

close = []
walletEMA = {"USDT": 1000, "BTC": 1}
walletbef = {"USDT": 1000, "BTC": 1}
closeP = pd.DataFrame
btcusdt = {}
# print(btcusdt['price'])
# print(client.get_exchange_info())

# print(buy(10))
# print(sell(0.00005))
# print(closeP['ema20'].iloc[49])

data()

emacross()