import asyncio, aiohttp, json
import datetime as datetime

class Alpaca_Account:
    '''This class will have everything to do with the users account including placing orders'''

    def __init__(self, member_id, live_key, live_secret, sandbox_key, sandbox_secret):
        #initialize variable with params/args
        self.member_id = member_id
        self.live_key = live_key
        self.live_secret = live_secret
        self.sandbox_key = sandbox_key
        self.sandbox_secret = sandbox_secret
        self.live_url = 'https://api.alpaca.markets/'
        self.paper_url = 'https://paper-api.alpaca.markets/'
    

    async def get_account(self, live = True):
        '''This param/arg will be determined by the prefix in the discord module. If the user chooses the live prefix
        live == True, if they choose the paper prefix live == False'''

        if live == True:
            return
        
        elif live == False:
            return
    

    async def order(self, side, symbol, qty, type = 'market', tif = 'gtc', funds = False, live = True):
        
        #qty of shares in live acct
        if funds == False and live == True: 
            if side == 'sell':
                return
            
            elif side == 'buy':
                return
        
        #dollar amt worth of shares in live acct
        elif funds == True and live == True:
            if side == 'sell':
                return
            
            elif side == 'buy':
                return
        
        #qty of shares in paper acct
        elif funds == False and live == False:
            if side == 'sell':
                return
            
            elif side == 'buy':
                return
        
        #dollar amt worth of shares in paper acct
        elif funds == True and live == False:
            if side == 'sell':
                return
            
            elif side == 'buy':
                return
        return 
    
   
    async def get_orders(self, live = True):
        #live account
        if live == True:
            async with aiohttp.ClientSession() as session:
                    async with session.get(f'{self.live_url}v2/orders') as request:
                        await request
        
        #paper account
        if live == False:
            async with aiohttp.ClientSession() as session:
                    async with session.get(f'{self.paper_url}v2/orders') as request:
                        await request
        return
    

    async def get_order(self, id, live = True):
        #live account
        if live == True:
            async with aiohttp.ClientSession() as session:
                    async with session.get(f'{self.live_url}v2/orders/{id}') as request:
                        await request
        
        #paper account
        if live == False:
            async with aiohttp.ClientSession() as session:
                    async with session.get(f'{self.paper_url}v2/orders/{id}') as request:
                        await request
        return
    

    async def get_asset(self, symbol, live = True):
        #live account
        if live == True:
            async with aiohttp.ClientSession() as session:
                    async with session.get(f'{self.live_url}v2/assets/{symbol.upper()}') as request:
                        await request
        
        #paper account
        if live == False:
            async with aiohttp.ClientSession() as session:
                    async with session.get(f'{self.paper_url}v2/assets/{symbol.upper()}') as request:
                        await request
        return