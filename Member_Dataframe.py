import pandas as pd
import discord as dc
import asyncio
import aiofiles
import json
from aiocsv import AsyncReader, AsyncDictReader, AsyncWriter, AsyncDictWriter

class Member_Data():

    def __init__(self):
        #create dictionary
        self.user_df = pd.DataFrame({"ID": '', "Name": '', "Live_Key": '', "Live_Secret": '', "Paper_Key": '', "Paper_Secret": ''}, index = [0])
        self.user_dictionary ={} #dictionary version of the dataframe that we write to the csv file

    #update rows, index, and values
    async def update_id(self, id, name):
        '''This class will be called when a user first joins the server, it will capture their name and id'''

        self.user_df = pd.DataFrame(self.user_df.append({"ID": id, "Name": name, "Live_Key": '', "Live_Secret": '', "Paper_Key": '', "Paper_Secret": ''}, ignore_index=True))
        #set the index to the user's id
        self.user_df.index = [item for item in self.user_df['ID']]
        #convert dataframe into dict to asynchronously write it to a csv file
        self.user_dictionary = self.user_df.to_dict()
        await self.update_csv()
        return self.user_df
        
    
    async def update_keys(self, id, live_key, live_secret, paper_key, paper_secret):
        '''id param will only be used for indexing
        This class will be called when a user dms the bot the proper command to store its alpaca keys. it will find 
        them in the dataframe by id and add the alpaca keys to  the proper panda column via arg order.
        '''

        #read in the full file and convert the dictionary into a pandas df
        dictionary = await self.read_csv()

        self.user_df.at[id, 'Live_Key'] = str(live_key)
        self.user_df.at[id, 'Live_Secret'] = str(live_secret)
        self.user_df.at[id, 'Paper_Key'] = str(paper_key)
        self.user_df.at[id, 'Paper_Secret'] = str(paper_secret)

        #convert dataframe into dict to asynchronously write it to a csv file
        self.user_dictionary = self.user_df.to_dict()
        await self.update_csv()
        return self.user_df.to_dict()
    
    
    async def read_csv(self):
        async with aiofiles.open('members_alpaca.csv', 'r') as f:
            self.user_dictionary = await f.read(json.loads(self.user_dictionary))
            #return self.user_dictionary so we can assign this function to a variable
            return self.user_dictionary
    
    
    async def update_csv(self):
        async with aiofiles.open('members_alpaca.csv', 'w') as f:
            await f.write(f'{json.dumps(self.user_dictionary)}\n')



users = Member_Data()
# print(users.user_df)
asyncio.run(users.update_id(123, 'george'))
asyncio.run(users.update_id(124, 'george'))
# print('\n')
# asyncio.run(users.update_keys(123, 1, 1, 1, 1))
# asyncio.run(users.update_keys(124, 1, 1, 1, 1))
# users.base_df()
# print(users.updated_df('g'))
# print(users.updated_df('gg'))
# print(users.user_df)