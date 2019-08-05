import asyncio
import ccxt.async_support as ccxt
import time

e = ccxt.binance()

async def load_markets(exchange):
    await exchange.fetch_markets()

async def fetch_ohlcv_async(exchange, symbol, counter = None):
    start = time.time()
    data = await exchange.fetch_ohlcv(symbol, '1d')
    print('{} fetch completed in {} seconds.'.format(counter,(time.time() - start).round(2)))
    await exchange.close()

ioloop = asyncio.get_event_loop()
ioloop.run_until_complete((load_markets(e)))

tasks = [ioloop.create_task(fetch_ohlcv_async(exchange, symbol, counter)) for i, symbol in enumerate(e.markets, 1)]
wait_tasks = asyncio.wait(tasks)
ioloop.run_until_complete(wait_tasks)
ioloop.close()
