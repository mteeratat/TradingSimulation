# https://python-binance.readthedocs.io/en/latest/
# https://algotrading101.com/learn/binance-python-api-guide/
# https://binance-docs.github.io/apidocs/spot/en/#general-info

import os
from binance.client import Client
import time
import pandas as pd

api_key = os.environ.get('binance_api')
api_secret = os.environ.get('binance_secret')

client = Client(api_key, api_secret)

# while(True):
#     time.sleep(10)
#     btcusdt = client.get_symbol_ticker(symbol='BTCUSDT')
    # print(btcusdt)

close = []
capital = 1000

candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1HOUR)
print(len(candles))
# print(candles)
for c in candles:
    close.append(c[4])

# print(close)

closeP = pd.DataFrame({'price': close})
closeP['ema'] = closeP['price'].ewm(span=20, adjust=False).mean()
print(closeP)
btcusdt = client.get_symbol_ticker(symbol='BTCUSDT')
print(btcusdt['price'])
print(client.get_exchange_info())