import asyncio, aiohttp, json, requests
import datetime as datetime
import pprint as p
from config import *

class Alpaca_Account:
    '''This class will have everything to do with the users account including placing orders'''

    def __init__(self, live_key, live_secret, paper_key, paper_secret):
        #initialize variable with params/args
        self.live_key = live_key
        self.live_secret = live_secret
        self.paper_key = paper_key
        self.paper_secret = paper_secret
        self.live_headers = {'APCA-API-KEY-ID': self.live_key, 'APCA-API-SECRET-KEY': self.live_secret}
        self.paper_headers = {'APCA-API-KEY-ID': self.paper_key, 'APCA-API-SECRET-KEY': self.paper_secret}
        self.live_url = 'https://api.alpaca.markets'
        self.paper_url = 'https://paper-api.alpaca.markets'
        self.response_dict = {} #universal dict for storing responses to send back to user
        #response data for the json responses of our different functions
        self.entry_price = ''
        self.side = ''
        self.shares = ''
        self.order_id = ''
        self.order_response = [] #for get orders to loop through responses to get_orders and their ids


    async def get_account(self, live=True):
        '''This param/arg will be determined by the prefix in the discord module. If the user chooses the live prefix
        live == True, if they choose the paper prefix live == False'''

        if live == True:
            async with aiohttp.ClientSession(headers=self.live_headers) as session:
                    async with session.get(f'{self.live_url}/v2/account') as resp:
                        response = await resp.json()
                        self.response_dict = response 
        
        elif live == False:
            async with aiohttp.ClientSession(headers=self.paper_headers) as session:
                    async with session.get(f'{self.paper_url}/v2/account') as resp:
                        response = await resp.json()
                        self.response_dict = response                       
    

    async def get_quote(self, symbol):
        url = f'https://data.alpaca.markets/v2/stocks/{symbol.upper()}/quotes/latest'
        async with aiohttp.ClientSession(headers=self.live_headers) as session:
            async with session.get(url) as resp:
                response = await resp.json()
                self.response_dict = response
                self.bid_price = response['quote']['bp']
                self.ask_price = response['quote']['ap']
    

    async def send_order(self, side, symbol, qty, take_profit='', stop_loss='', limit = '', tif = 'gtc', live = True):
        
        #if limit, take, or stop arent specified it will default as a market order with not take or stop price
        if not limit and not stop_loss and not take_profit:
            data = {'symbol': symbol.upper(), 'qty': float(qty), 'side': side, 'type': 'market', 'time_in_force': tif}
        #limit order without take profit or stop price
        elif limit and not stop_loss and not take_profit:
            data = {'symbol': symbol.upper(), 'qty': float(qty), 'side': side, 'type': 'limit', 'time_in_force': tif, 
            'limit_price': float(limit)}
        #if limit not spcified but take and loss are it will be a market bracket order
        elif not limit and stop_loss and take_profit:
            data = { "side": side, "symbol": symbol.upper(), "type": "market", "qty": float(qty), "time_in_force": tif,   
            "order_class": "bracket", "take_profit": {"limit_price": take_profit},   
            "stop_loss": {"stop_price": stop_loss} }
        #if limit take and stop are specified it will be a limit bracker order
        elif limit and stop_loss and take_profit:
            data = { "side": side, "symbol": symbol.upper(), "type": "limit", "qty": float(qty), "time_in_force": tif,   
            'limit_price': float(limit), "order_class": "bracket", "take_profit": {"limit_price": take_profit},   
            "stop_loss": {"stop_price": stop_loss} }
        
        #live account post request
        if live == True: 
            url = f'{self.live_url}/v2/orders'

            async with aiohttp.ClientSession(headers=self.live_headers) as session:
                async with session.post(url, json=data) as resp:
                    response = await resp.json()
                    self.response_dict = response
                    print(response)
               
        
        #paper account post request
        elif live == False:
            url = f'{self.paper_url}/v2/orders'
                        
            async with aiohttp.ClientSession(headers=self.paper_headers) as session:
                async with session.post(url, json=data) as resp:
                    response = await resp.json()
                    self.response_dict = response
                    p.pprint(response)

   
    async def get_orders(self, status='open', live=True):

        #live account
        if live == True:
            async with aiohttp.ClientSession(headers=self.live_headers) as session:
                    async with session.get(f'{self.live_url}/v2/orders?status={status}') as resp:
                        self.order_response = await resp.json()
                        p.pprint(self.order_response)
        
        #paper account
        if live == False:
            async with aiohttp.ClientSession(headers=self.paper_headers) as session:
                    async with session.get(f'{self.paper_url}/v2/orders?status={status}') as resp:
                        self.order_response = await resp.json()
                        p.pprint(self.order_response)
        
        if not self.order_response:
            if status == 'closed':
                self.order_response = [{'orders': 'You have 0 closed orders'}]
            elif status == 'open':
                self.order_response = [{'orders': 'You have 0 open orders'}]
            elif status == 'all':
                self.order_response = [{'orders': 'You have neither any open or closed orders'}]


    async def get_position(self, symbol, live=True):

        #live account
        if live == True:
            async with aiohttp.ClientSession(headers=self.live_headers) as session:
                    async with session.get(f'{self.live_url}/v2/positions/{symbol.upper()}') as resp:
                        response = await resp.json()
                        self.response_dict = response
        
        #paper account
        if live == False:
            async with aiohttp.ClientSession(headers=self.paper_headers) as session:
                    async with session.get(f'{self.paper_url}/v2/positions/{symbol.upper()}') as resp:
                        response = await resp.json()
                        self.response_dict = response
        
        self.entry_price = float(response['avg_entry_price'])
        self.side = response['side']
        self.shares = float(response['qty'])
    

    async def get_all_positions(self, live=True):
        
        #live account
        if live == True:
            async with aiohttp.ClientSession(headers=self.live_headers) as session:
                    async with session.get(f'{self.live_url}/v2/positions') as resp:
                        response = await resp.json()
                        self.response_dict = response
                        print(response)
        
        #paper account
        if live == False:
            async with aiohttp.ClientSession(headers=self.paper_headers) as session:
                    async with session.get(f'{self.paper_url}/v2/positions') as resp:
                        response = await resp.json()
                        self.response_dict = response
                        p.pprint(response)


    async def close_position(self, symbol, qty='', live=True):
            
            #live account
            if live == True:

                if '%' not in str(qty) and qty != '':
                    url = f'{self.live_url}/v2/positions/{symbol.upper()}?qty={qty}'
                elif '%' in str(qty) and qty != '':
                    url = f'{self.live_url}/v2/positions/{symbol.upper()}?percentage={qty.strip("%")}'
                else:
                    url = f'{self.live_url}/v2/positions/{symbol.upper()}'
                
                async with aiohttp.ClientSession(headers=self.live_headers) as session:
                        async with session.delete(url) as resp:
                            response = await resp.json()
                            self.response_dict = response
                            print(response)
            
            #paper account
            if live == False:

                if '%' not in str(qty) and qty != '':
                    url = f'{self.paper_url}/v2/positions/{symbol.upper()}?qty={qty}'
                elif '%' in str(qty) and qty != '':
                    url = f'{self.paper_url}/v2/positions/{symbol.upper()}?percentage={qty.strip("%")}'
                else:
                    url = f'{self.paper_url}/v2/positions/{symbol.upper()}'
                
                async with aiohttp.ClientSession(headers=self.paper_headers) as session:
                        async with session.delete(url) as resp:
                            response = await resp.json()
                            self.response_dict = response
                            p.pprint(response)


    async def close_all_positions(self, live=True):
        
        #live account
        if live == True:
            async with aiohttp.ClientSession(headers=self.live_headers) as session:
                    async with session.delete(f'{self.live_url}/v2/positions') as resp:
                        response = await resp.json()
                        self.response_dict = response
                        print(response)
        
        #paper account
        if live == False:
            async with aiohttp.ClientSession(headers=self.paper_headers) as session:
                    async with session.delete(f'{self.paper_url}/v2/positions') as resp:
                        response = await resp.json()
                        self.response_dict = response
                        p.pprint(response)


    async def get_order(self, id, live = True):
        #live account
        if live == True:
            async with aiohttp.ClientSession(headers=self.live_headers) as session:
                    async with session.get(f'{self.live_url}/v2/orders/{id}') as resp:
                        response = await resp.json()
                        self.response_dict = response
                        print(response)
        
        #paper account
        if live == False:
            async with aiohttp.ClientSession(headers=self.paper_headers) as session:
                    async with session.get(f'{self.paper_url}/v2/orders/{id}') as resp:
                        response = await resp.json()
                        self.response_dict = response
                        print(response)                      


    async def get_asset(self, symbol, live = True):
        #live account
        if live == True:
            async with aiohttp.ClientSession(headers=self.live_headers) as session:
                    async with session.get(f'{self.live_url}/v2/assets/{symbol.upper()}') as resp:
                        response = await resp.json()
                        self.response_dict = response
                        print(response)
        
        #paper account
        if live == False:
            async with aiohttp.ClientSession(headers=self.paper_headers) as session:
                    async with session.get(f'{self.paper_url}/v2/assets/{symbol.upper()}') as resp:
                        response = await resp.json()
                        self.response_dict = response
                        print(response)


    async def stop_loss(self, symbol, stop_perc, qty='', tif = 'gtc', live = True):
        
        #check information on open position. This will make self.entry_price == the avg entry price in the position
        await self.get_position(symbol.upper(), live)

        #if elif statement to decide between default amount of shares to take profit or a selected amount
        if qty == '':
            qty = self.shares
        elif qty != '':
            qty = float(qty)
        
        #adjust json data based on position side info
        if self.side == 'long':
            data = {'symbol': symbol.upper(), 'qty': qty, 'side': 'sell', 'type': 'stop', 'time_in_force': tif,
                    'stop_price': self.entry_price * float(stop_perc) }
        elif self.side == 'short':
            data = {'symbol': symbol.upper(), 'qty': qty, 'side': 'buy', 'type': 'stop', 'time_in_force': tif, 
                    'stop_price': self.entry_price * float(stop_perc) }
         
         ###
            
        #live account post request
        if live == True: 
            url = f'{self.live_url}/v2/orders'
        
            async with aiohttp.ClientSession(headers=self.live_headers) as session:
                async with session.post(url, json=data) as resp:
                    response = await resp.json() 
                    self.response_dict = response
                    print(response)                          

        #paper account post request
        elif live == False:
            url = f'{self.paper_url}/v2/orders'

            async with aiohttp.ClientSession(headers=self.paper_headers) as session:
                async with session.post(url, json=data) as resp:
                    response = await resp.json()
                    self.response_dict = response 
                    print(response)


    async def take_profit(self, symbol, stop_perc, qty='', tif = 'gtc', live = True):
        
        #check information on open position. This will make self.entry_price == the avg entry price in the position
        await self.get_position(symbol.upper(), live)

        #if elif statement to decide between default amount of shares to take profit or a selected amount
        if qty == '':
            qty = self.shares
        elif qty != '':
            qty = float(qty)
        
        #adjust json data based on position info
        if self.side == 'long':
            data = {'symbol': symbol.upper(), 'qty': qty, 'side': 'sell', 'type': 'limit', 'time_in_force': tif,
                    'limit_price': self.entry_price * float(stop_perc) }
        elif self.side == 'short':
            data = {'symbol': symbol.upper(), 'qty': qty, 'side': 'buy', 'type': 'limit', 'time_in_force': tif, 
                    'limit_price': self.entry_price * float(stop_perc) }
         
         ###
            
        #live account post request
        if live == True: 
            url = f'{self.live_url}/v2/orders'
        
            async with aiohttp.ClientSession(headers=self.live_headers) as session:
                async with session.post(url, json=data) as resp:
                    response = await resp.json() 
                    self.response_dict = response
                    print(response)                          

        #paper account post request
        elif live == False:
            url = f'{self.paper_url}/v2/orders'

            async with aiohttp.ClientSession(headers=self.paper_headers) as session:
                async with session.post(url, json=data) as resp:
                    response = await resp.json() 
                    self.response_dict = response
                    print(response)


    async def cancel_orders(self, live = True):
        #live account
        if live == True:
            async with aiohttp.ClientSession(headers=self.live_headers) as session:
                    async with session.delete(f'{self.live_url}/v2/orders') as resp:
                        response = await resp.json()
                        self.response_dict = response
                        print(response)
        
        #paper account
        if live == False:
            async with aiohttp.ClientSession(headers=self.paper_headers) as session:
                    async with session.delete(f'{self.paper_url}/v2/orders') as resp:
                        response = await resp.json()
                        self.response_dict = response
                        print(response)


    async def cancel_order(self, symbol, live = True):
        
        await self.get_orders('open',live=False)
        
        #loop through all the orders to find the order that matches the symbol we are looking for
        for order in self.order_response:
            if order['symbol'] == symbol.upper():
                order_id = order['id']
        
        #live account
        if live == True:
            async with aiohttp.ClientSession(headers=self.live_headers) as session:
                    async with session.delete(f'{self.live_url}/v2/orders/{order_id}') as resp:
                        response = await resp.json()
                        print(response)
        
        #paper account
        if live == False:
            async with aiohttp.ClientSession(headers=self.paper_headers) as session:
                    async with session.delete(f'{self.paper_url}/v2/orders/{order_id}') as resp:
                        response = await resp.json()
                        print(response)


    async def trailing_stop(self, symbol, stop_amt, qty='', tif = 'gtc', live = True):
        
        #check information on open position. This will make self.entry_price == the avg entry price in the position
        await self.get_position(symbol.upper(), live)

        #if elif statement to decide between default amount of shares to take profit or a selected amount
        if qty == '':
            qty = self.shares
        elif qty != '':
            qty = float(qty)
        
        #adjust json data based on position side info
        if self.side == 'long':
            if '%' in str(stop_amt):
                data = {'symbol': symbol.upper(), 'qty': qty, 'side': 'sell', 'type': 'trailing_stop', 'time_in_force': tif,
                        'trail_percent': float(stop_amt.strip('%')) }
            elif '%' not in str(stop_amt):
                data = {'symbol': symbol.upper(), 'qty': qty, 'side': 'sell', 'type': 'trailing_stop', 'time_in_force': tif,
                        'trail_price': float(stop_amt) }
        elif self.side == 'short':
            if '%' in str(stop_amt):
                data = {'symbol': symbol.upper(), 'qty': qty, 'side': 'buy', 'type': 'trailing_stop', 'time_in_force': tif,
                        'trail_percent': float(stop_amt.strip('%')) }
            elif '%' not in str(stop_amt):
                data = {'symbol': symbol.upper(), 'qty': qty, 'side': 'buy', 'type': 'trailing_stop', 'time_in_force': tif,
                        'trail_price': float(stop_amt) }
         
         ###
            
        #live account post request
        if live == True: 
            url = f'{self.live_url}/v2/orders'
        
            async with aiohttp.ClientSession(headers=self.live_headers) as session:
                async with session.post(url, json=data) as resp:
                    response = await resp.json() 
                    self.response_dict = response
                    print(response)                          

        #paper account post request
        elif live == False:
            url = f'{self.paper_url}/v2/orders'
            r = requests.post(url, headers=self.paper_headers, json=data)
            resp = r.json()
            print(resp)

            # async with aiohttp.ClientSession(headers=self.paper_headers) as session:
            #     async with session.post(url, json=data) as resp:
            #         response = await resp.json()
            #         self.response_dict = response 
            #         print(response)


if __name__ == '__main__':
    # lim = ''
    # if not lim:
    #     print('hello')
    a = Alpaca_Account(l_key, l_secret, p_key, p_secret)
    asyncio.run(a.trailing_stop('aapl', '.95%', live=False))
    # asyncio.run(a.cancel_order('aapl',live=False))
