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
        self.live_url = 'https://api.alpaca.markets'
        self.paper_url = 'https://paper-api.alpaca.markets'
    

    async def get_account(self, acct_type):
        '''This param/arg will be determined by the prefix in the discord module. If the user chooses the live prefix
        we will call this function with the string "live". If they choose the paper prefix we will pass "Paper". '''

        if acct_type == 'live':
            return
        
        elif acct_type == 'paper':
            return
    

    async def order(self, side, symbol, qty, type = 'market', tif = 'gtc', funds = False, live = True):
        
        if funds == False and live == True: 
            if side == 'sell':
                return
            
            elif side == 'buy':
                return
        
        elif funds == True and live == True:
            if side == 'sell':
                return
            
            elif side == 'buy':
                return
        
        elif funds == False and live == False:
            if side == 'sell':
                return
            
            elif side == 'buy':
                return
        
        elif funds == True and live == False:
            if side == 'sell':
                return
            
            elif side == 'buy':
                return
        return 