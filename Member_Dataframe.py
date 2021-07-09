import pandas as pd
import discord as dc

class Member_Data():

    def __init__(self):
        #create dictionary
        self.user_df = pd.DataFrame({"ID": '', "Name": '', "Live_Key": '', "Live_Secret": '', "Paper_Key": '', "Paper_Secret": ''}, index = [0])


    #update rows, index, and values
    def update_id(self, id, name):
        '''This class will be called when a user first joins the server, it will capture their name and id'''

        self.user_df = pd.DataFrame(self.user_df.append({"ID": id, "Name": name, "Live_Key": '', "Live_Secret": '', "Paper_Key": '', "Paper_Secret": ''}, ignore_index=True))
        self.user_df.index = [item for item in self.user_df['ID']]
        print(self.user_df)
        # print(f'USER DF  {self.user_df}  END USER DF')
        # return self.user_df
    
    def update_keys(self, id, live_key, live_secret, paper_key, paper_secret):
        '''id param will only be used for indexing
        This class will be called when a user dms the bot the proper command to store its alpaca keys. it will find 
        them in the dataframe by id and add the alpaca keys to  the proper panda column via arg order.
        '''
        self.user_df.at[id, 'Live_Key'] = str(live_key)
        self.user_df.at[id, 'Live_Secret'] = str(live_secret)
        self.user_df.at[id, 'Paper_Key'] = str(paper_key)
        self.user_df.at[id, 'Paper_Secret'] = str(paper_secret)
        return self.user_df



users = Member_Data()
# print(users.user_df)
(users.update_id(123, 'george'))
print('\n')
print(users.update_keys(123, 1, 1, 1, 1))
# users.base_df()
# print(users.updated_df('g'))
# print(users.updated_df('gg'))
# print(users.user_df)