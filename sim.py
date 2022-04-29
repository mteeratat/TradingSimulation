# https://python-binance.readthedocs.io/en/latest/
# https://algotrading101.com/learn/binance-python-api-guide/
# https://binance-docs.github.io/apidocs/spot/en/#general-info

import os
from binance.client import Client
import time
import pandas as pd
from multiprocessing import Process
import logging
# import sys
import urllib3

def data():
    global closeP
    close = []
    candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1MINUTE, limit=50)
    # print(len(candles))
    for c in candles:
        close.append(float(c[4]))
    closeP = pd.DataFrame({'price': close})
    closeP['ema20'] = closeP['price'].ewm(span=20, adjust=False).mean()
    closeP['ema50'] = closeP['price'].ewm(span=50, adjust=False).mean()
    # print(closeP.iloc[49])

def buy(amount, wallet):
    wallet["USDT"] -= amount
    wallet["BTC"] += amount/closeP['price'].iloc[49]
    print("buy")
    return wallet

def sell(amount, wallet):
    wallet["BTC"] -= amount
    wallet["USDT"] += amount*closeP['price'].iloc[49]
    print("sell")
    return wallet

def emacross():
    print("emacross START!")
    count = 0
    while(True):

        # while(closeP['price'].iloc[49] > closeP['ema50'].iloc[49]):
            # print("bullish1")
        if closeP['ema20'].iloc[49] > closeP['ema50'].iloc[49] and count == 0:
            print(buy(10, walletEMA))
            count = 1
                # break
            # data()
            # time.sleep(10)

        # while(closeP['price'].iloc[49] < closeP['ema50'].iloc[49]):
            # print("bearish1")
        if closeP['ema20'].iloc[49] < closeP['ema50'].iloc[49] and count == 1:
            print(sell(0.01, walletEMA))
            count = 0
                # break
            # data()
            # time.sleep(10)

        print(walletEMA)
        # sys.stdout.flush()
        # logging.info(walletEMA)
        data()
        time.sleep(10)

def befema():
    print("befema START!")
    while(True):

        while(closeP['ema20'].iloc[49] < closeP['ema50'].iloc[49]):
            # print("bearish2")
            if closeP['price'].iloc[49] > closeP['ema50'].iloc[49]:
                print(buy(10, walletbef))
                break
            print(walletbef)
            # sys.stdout.flush()
            # logging.info(walletbef)
            data()
            time.sleep(10)

        count = 0
        while(closeP['ema20'].iloc[49] > closeP['ema50'].iloc[49]):
            # print("bullish2")
            if closeP['price'].iloc[49] < closeP['ema20'].iloc[49] and count == 0:
                print(sell(0.005, walletbef))
                count = 1
            if closeP['price'].iloc[49] < closeP['ema50'].iloc[49] and count == 1:
                print(sell(0.005, walletbef))
                break
            print(walletbef)
            # sys.stdout.flush()
            # logging.info(walletbef)
            data()
            time.sleep(10)

        # print(walletbef)
        # sys.stdout.flush()
        logging.info(walletbef)
        data()
        time.sleep(10)

logging.basicConfig(level=logging.INFO)
# urllib3.disable_warnings()

api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')

client = Client(api_key, api_secret)

close = []
walletEMA = {"name": "emacross", "USDT": 1000, "BTC": 1}
walletbef = {"name": "befema", "USDT": 1000, "BTC": 1}
closeP = pd.DataFrame

data()

# emacross()

if __name__ == '__main__':
    p1 = Process(target=emacross)
    p2 = Process(target=befema)

    p1.start()
    p2.start()

    p1.join()
    p2.join()