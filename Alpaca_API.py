import asyncio, aiohttp, json, requests
import datetime as datetime

class Alpaca_Account:
    '''This class will have everything to do with the users account including placing orders'''

    def __init__(self, member_id, live_key, live_secret, paper_key, paper_secret):
        #initialize variable with params/args
        self.member_id = member_id
        self.live_key = live_key
        self.live_secret = live_secret
        self.paper_key = paper_key
        self.paper_secret = paper_secret
        self.live_headers = {'APCA-API-KEY-ID': self.live_key, 'APCA-API-SECRET-KEY': self.live_secret}
        self.paper_headers = {'APCA-API-KEY-ID': self.paper_key, 'APCA-API-SECRET-KEY': self.paper_secret}
        self.live_url = 'https://api.alpaca.markets'
        self.paper_url = 'https://paper-api.alpaca.markets'
        self.responses_dict = {} #universal dict for storing responses to send back to user
    

    async def get_account(self, live=True):
        '''This param/arg will be determined by the prefix in the discord module. If the user chooses the live prefix
        live == True, if they choose the paper prefix live == False'''

        if live == True:
            async with aiohttp.ClientSession(headers=self.live_headers) as session:
                    async with session.get(f'{self.live_url}/v2/account') as resp:
                        response = await resp.json()
                        print(response)
        
        elif live == False:
            async with aiohttp.ClientSession(headers=self.paper_headers) as session:
                    async with session.get(f'{self.paper_url}/v2/account') as resp:
                        response = await resp.json()
                        print(response)
            return
    

    async def send_order(self, side, symbol, qty, limit = 0, tif = 'gtc', live = True):
        
        #if limit isn't specified it will default as a market order
        if limit == 0:
            data = {'symbol': symbol.upper(), 'qty': qty, 'side': side, 'type': 'market', 'time_in_force': tif}
        else:
            data = {'symbol': symbol.upper(), 'qty': qty, 'side': side, 'type': 'limit', 'time_in_force': tif, 'limit_price': limit}
        
        #live account post request
        if live == True: 
            url = f'{self.live_url}/v2/orders'
            
            if side == 'sell':
                async with aiohttp.ClientSession(headers=self.live_headers) as session:
                    async with session.post(url, json=data) as resp:
                        response = await resp.json() 
                        print(response)                          
            elif side == 'buy':
                async with aiohttp.ClientSession(headers=self.live_headers) as session:
                    async with session.post(url, json=data) as resp:
                        response = await resp.json()
                        print(response)
               
        
        #paper account post request
        elif live == False:
            url = f'{self.paper_url}/v2/orders'
            
            if side == 'sell':
                async with aiohttp.ClientSession(headers=self.paper_headers) as session:
                    async with session.post(url, json=data) as resp:
                        response = await resp.json() 
                        print(response)
            elif side == 'buy':
                async with aiohttp.ClientSession(headers=self.paper_headers) as session:
                    async with session.post(url, json=data) as resp:
                        response = await resp.json()
                        print(response)
                 
   
    async def get_orders(self, live=True):
        #live account
        if live == True:
            async with aiohttp.ClientSession(headers=self.live_headers) as session:
                    async with session.get(f'{self.live_url}/v2/orders') as resp:
                        response = await resp.json()
                        print(response)
        
        #paper account
        if live == False:
            async with aiohttp.ClientSession(headers=self.paper_headers) as session:
                    async with session.get(f'{self.paper_url}/v2/orders') as resp:
                        response = await resp.json()
                        print(response)
        return
    

    async def get_order(self, id, live = True):
        #live account
        if live == True:
            async with aiohttp.ClientSession(headers=self.live_headers) as session:
                    async with session.get(f'{self.live_url}/v2/orders/{id}') as resp:
                        response = await resp.json()
                        print(response)
        
        #paper account
        if live == False:
            async with aiohttp.ClientSession(headers=self.paper_headers) as session:
                    async with session.get(f'{self.paper_url}/v2/orders/{id}') as resp:
                        response = await resp.json()
                        print(response)
        return
    

    async def get_asset(self, symbol, live = True):
        #live account
        if live == True:
            async with aiohttp.ClientSession(headers=self.live_headers) as session:
                    async with session.get(f'{self.live_url}/v2/assets/{symbol.upper()}') as resp:
                        response = await resp.json()
                        print(response)
        
        #paper account
        if live == False:
            async with aiohttp.ClientSession(headers=self.paper_headers) as session:
                    async with session.get(f'{self.paper_url}/v2/assets/{symbol.upper()}') as resp:
                        response = await resp.json()
                        print(response)



a = Alpaca_Account(1, 'AKONGGIJ6V3OMHMIGHON', 'Bf65kFJS0OixniK71p91GB0EPI0W0YKxAgSLmL7n', 'PKM63NQX8JLSSN76IM6P', 'Xs15aW1jXzLHI2duQ6QjyRNsFtIP34rOEDbCgGH8')

asyncio.run(a.get_account(live=False))
# data = {'symbol': 'AAPL', 'qty': 2, 'side': 'buy', 'type': 'market', 'time_in_force': 'gtc'}
# url = f'{a.paper_url}/v2/orders'
# r = requests.post(url, headers = a.paper_headers, json=data)
# print(r.json())