import pandas as pd
import discord as dc

class Broker_Member():

    def __init__(self):
        #create dictionary
        self.user_df = {"ID": '', "Name": '', "Live Key": '', "Live Secret": '', "Sandbox Key": '', "Sandbox Secret": ''}

    #create member dataframe
    def base_df(self):
        #create dataframe from dictionary
        self.user_df = pd.DataFrame(self.user_df)
        print(self.user_df)
        return self.user_df


    #update rows, index, and values
    def update_df(self, id):
        self.user_df = pd.DataFrame(self.user_df.append({"users": id, "attempts": 0, "last_query": 0, "next_query": 0}, ignore_index=True))
        self.user_df.index = [item for item in self.user_df['ID']]
        print(self.user_df)
        # print(f'USER DF  {self.user_df}  END USER DF')
        # return self.user_df



users = user_df()
# users.base_df()
# print(users.updated_df('g'))
# print(users.updated_df('gg'))
# print(users.user_df)