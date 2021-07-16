import pandas as pd
import discord as dc
import asyncio
import aiofiles
import json
from aiocsv import AsyncReader, AsyncDictReader, AsyncWriter, AsyncDictWriter

class Member_Alpaca_Data():

    def __init__(self):
        #create dictionary
        self.user_df = pd.DataFrame()
        self.user_dictionary = {} #dictionary version of the dataframe that we write to the csv file

    #update rows, index, and values
    async def update_id(self, id, name):
        '''This class will be called when a user first joins the server, it will capture their name and id'''

        await self.read_csv()
        
        # #conditions for if there are values in the file
        if id in self.user_dictionary.keys():
            #create nested dict
            self.user_dictionary[id] = {}
            #update nested dict
            self.user_dictionary[id]['id'] = id
            self.user_dictionary[id]['name'] = name
        
    
        elif id not in self.user_dictionary.keys():
            #create nested dict
            self.user_dictionary[id] = {}
            #update nested dict
            self.user_dictionary[id]['id'] = id
            self.user_dictionary[id]['name'] = name
        
        await self.update_csv()
        
        
    
    async def update_keys(self, id, live_key, live_secret, paper_key, paper_secret):
        '''id param will only be used for indexing
        This class will be called when a user dms the bot the proper command to store its alpaca keys. it will find 
        them in the dataframe by id and add the alpaca keys to  the proper panda column via arg order.
        '''

        #read in the full file and convert the dictionary into a pandas df
        await self.read_csv()
        
        #update the user's keys by indexing their id number.
        self.user_dictionary[id]['Live_Key'] = (live_key)
        self.user_dictionary[id]['Live_Secret'] = (live_secret)
        self.user_dictionary[id]['Paper_Key'] = (paper_key)
        self.user_dictionary[id]['Paper_Secret'] = (paper_secret)
        
        #convert dataframe into dict to asynchronously write it to a csv file
        await self.update_csv()
        
    
    
    async def read_csv(self):
        async with aiofiles.open('members_alpaca.csv', 'r') as f:
            self.user_dictionary = await f.read()
            
            if not self.user_dictionary:
                self.user_dictionary = dict(self.user_dictionary)
            if self.user_dictionary:
                self.user_dictionary = json.loads(self.user_dictionary)
            return self.user_dictionary
            
    
    
    async def update_csv(self):
        async with aiofiles.open('members_alpaca.csv', 'w') as f:
            await f.write(json.dumps(self.user_dictionary))


if __name__ == '__main__':
    users = Member_Alpaca_Data()
    # print(users.user_df)
    # asyncio.run(users.update_id(126, 'george'))
    # asyncio.run(users.update_id(str(126), 'george'))
    # # print('\n')
    asyncio.run(users.update_keys(str(125), 1, 1, 1, 1))
    # asyncio.run(users.update_keys(str(124), 1, 1, 1, 1))
    # users.base_df()
    # print(users.updated_df('g'))
    # print(users.updated_df('gg'))
    # print(users.user_df)
    # asyncio.run(users.read_csv())

# def update_id(id, name):
#     '''This class will be called when a user first joins the server, it will capture their name and id'''
#     user_dictionary = {}
#     #conditions for if there are values in the file
#     if id in user_dictionary.keys():
#         #create nested dict
#         user_dictionary[id] = {}
#         #update nested dict
#         user_dictionary[id]['id'] = id
#         user_dictionary[id]['name'] = name
        
    
#     elif id not in user_dictionary.keys():
#         #create nested dict
#         user_dictionary[id] = {}
#         #update nested dict
#         user_dictionary[id]['id'] = id
#         user_dictionary[id]['name'] = name
    
#     print(user_dictionary)

# update_id('george', 'geo')