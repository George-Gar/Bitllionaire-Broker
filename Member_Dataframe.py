import pandas as pd
import discord as dc
import asyncio
import aiofiles
import json
from aiocsv import AsyncReader, AsyncDictReader, AsyncWriter, AsyncDictWriter

class Member_Data():

    def __init__(self):
        #create dictionary
        self.user_df = pd.DataFrame()
        self.user_dictionary = {} #dictionary version of the dataframe that we write to the csv file

    #update rows, index, and values
    async def update_id(self, id, name):
        '''This class will be called when a user first joins the server, it will capture their name and id'''

        await self.read_csv()
        
        #conditions for if there are values in the file
        if self.user_dictionary:
            #read dict into pandas, add new users, convert pandas to dict, write to csv
            self.user_df = pd.DataFrame.from_records(self.user_dictionary)
            self.user_df = pd.DataFrame(self.user_df.append({"ID": str(id), "Name": name, "Live_Key": '', "Live_Secret": '', "Paper_Key": '', "Paper_Secret": ''}, ignore_index=True))
            #set the index to the user's id
            self.user_df.index = [item for item in self.user_df['ID']] 
            #convert dataframe into dict to asynchronously write it to a csv file
            self.user_dictionary = self.user_df.to_dict()
            await self.update_csv()
        
        elif not self.user_dictionary:
            #create new pandas, convert into dict, write to csv
            self.user_df = pd.DataFrame(self.user_df.append({"ID": str(id), "Name": name, "Live_Key": '', "Live_Secret": '', "Paper_Key": '', "Paper_Secret": ''}, ignore_index=True))
            #set the index to the user's id
            self.user_df.index = [item for item in self.user_df['ID']]
            #convert dataframe into dict to asynchronously write it to a csv file
            self.user_dictionary = self.user_df.to_dict()
            await self.update_csv()
        
        
    
    async def update_keys(self, id, live_key, live_secret, paper_key, paper_secret):
        '''id param will only be used for indexing
        This class will be called when a user dms the bot the proper command to store its alpaca keys. it will find 
        them in the dataframe by id and add the alpaca keys to  the proper panda column via arg order.
        '''

        #read in the full file and convert the dictionary into a pandas df
        await self.read_csv()
        self.user_df = pd.DataFrame.from_records(self.user_dictionary)
        #update the user's keys by indexing their id number.
        self.user_df.at[id, 'Live_Key'] = str(live_key)
        self.user_df.at[id, 'Live_Secret'] = str(live_secret)
        self.user_df.at[id, 'Paper_Key'] = str(paper_key)
        self.user_df.at[id, 'Paper_Secret'] = str(paper_secret)
        
        #convert dataframe into dict to asynchronously write it to a csv file
        self.user_dictionary = self.user_df.to_dict()
        print(self.user_df)
        await self.update_csv()
        
    
    
    async def read_csv(self):
        async with aiofiles.open('members_alpaca.csv', 'r') as f:
            self.user_dictionary = await f.read()
            if self.user_dictionary:
                self.user_dictionary = json.loads(self.user_dictionary)
            
    
    
    async def update_csv(self):
        async with aiofiles.open('members_alpaca.csv', 'w') as f:
            await f.write(json.dumps(self.user_dictionary))



users = Member_Data()
# print(users.user_df)
asyncio.run(users.update_id(str(125), 'george'))
# asyncio.run(users.update_id(str(126), 'george'))
# # print('\n')
asyncio.run(users.update_keys(str(125), 1, 1, 1, 1))
# asyncio.run(users.update_keys(str(124), 1, 1, 1, 1))
# users.base_df()
# print(users.updated_df('g'))
# print(users.updated_df('gg'))
# print(users.user_df)
# asyncio.run(users.read_csv())