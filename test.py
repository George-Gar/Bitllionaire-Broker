from Alpaca_API import a   
import asyncio, aiohttp


# asyncio.run(a.send_order('buy', 'AAPL', 2, live=False))
print(a.entry_price)
# asyncio.run(a.stop_loss('aapl', 2, .90, live=False))