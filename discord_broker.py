from discord.ext.commands.core import command
from discord.ext import commands
from Alpaca_API import Alpaca_Account
from Member_Dataframe import Member_Alpaca_Data

#create the discord client as well as important channel variables
client = commands.Bot(command_prefix='!')
bit_screener = client.get_channel(842046148108746803)
print(bit_screener)

#write the bot functionality
@client.command(name='buy')
async def buy():
    return













#run client on server
client.run('ODY0OTk4MjA3OTI5NzEyNjQw.YO9mWw.7elqzkaRwMOwk57Uouw23SH8qdc')