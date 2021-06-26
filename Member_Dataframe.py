import pandas as pd
import discord as dc

class Member_Data():

    def __init__(self):
        #create dictionary
        self.user_df = pd.DataFrame({"ID": '', "Name": '', "Live_Key": '', "Live_Secret": '', "Sandbox_Key": '', "Sandbox_Secret": ''}, index = [0])


    #update rows, index, and values
    def update_id(self, id, name):
        self.user_df = pd.DataFrame(self.user_df.append({"ID": id, "Name": name, "Live_Key": '', "Live_Secret": '', "Sandbox_Key": '', "Sandbox_Secret": ''}, ignore_index=True))
        self.user_df.index = [item for item in self.user_df['ID']]
        print(self.user_df)
        # print(f'USER DF  {self.user_df}  END USER DF')
        # return self.user_df
    
    def update_keys(self, id, live_key, live_secret, sandbox_key, sandbox_secret):
        self.user_df.at[id, 'Live_Key'] = str(live_key)
        self.user_df.at[id, 'Live_Secret'] = str(live_secret)
        self.user_df.at[id, 'Sandbox_Key'] = str(sandbox_key)
        self.user_df.at[id, 'Sandbox_Secret'] = str(sandbox_secret)
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