
import asyncio
import ccxt
import ccxt.async_support
import ta
import time
import sqlite3
from datetime import datetime

time_period = 6 # in hours

conn = sqlite3.connect('raw_data.sqlite')
cur = conn.cursor()

cur.execute('DROP TABLE IF EXISTS Pairs')

cur.execute('''CREATE TABLE IF NOT EXISTS Pairs
            (id INTEGER PRIMARY KEY, symbol TEXT, timestamp REAL,
            open REAL, close REAL, high REAL, low REAL, volume REAL)''')

async def fetch_ticker_asinc(ticker = None):
    #if ticker is None : break
    binance = ccxt.async_support.binance()
    data = (await binance.fetch_ohlcv(symbol = ticker, timeframe = '1m', since = int(time.time()*1000) - time_period*3600000))
    return data


print('Connecting to binance exchange...\n')
binance = ccxt.binance()
binance.load_markets()

for market in binance.markets.keys():
    try:
        print('{} market:'.format(market))
        data = asyncio.get_event_loop().run_until_complete(fetch_ticker_asinc(market))
        for line in data:
            d, o, h, l, c, v = line
            d = datetime.fromtimestamp(d/1000)
            cur.execute('INSERT OR IGNORE INTO Pairs (symbol, timestamp, open, close , high, low, volume) VALUES(?, ?, ?, ?, ?, ?, ?)',
                            (market, d, o, c, h, l, v))
    except Exception as e:
        print("something goes wrong...\n")
        print(e, '\n')
    conn.commit()

cur.close()
