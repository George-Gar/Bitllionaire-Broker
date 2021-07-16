from discord.ext.commands.core import command
from discord.ext import commands
from Alpaca_API import Alpaca_Account
from Member_Dataframe import Member_Alpaca_Data

#create the discord client as well as important channel variables
client = commands.Bot(command_prefix='!')
bit_screener = client.get_channel(842046148108746803)

#write the bot functionality
@client.command(name='buy')
async def buy(ctx):
    #create instance of member_alpaca_data class
    member = Member_Alpaca_Data()
    await member.read_csv()
    print(member.user_dictionary) 
    return

@client.command(name='add')
async def add(ctx):
    #create instance of member_alpaca_data class
    member = Member_Alpaca_Data()
    #create the author object
    author = ctx.message.author
    await member.update_id(author.id, author.name)
    return

@client.command(name='register')
async def add(ctx, live_key, live_secret, paper_key, paper_secret):
    #create instance of member_alpaca_data class
    member = Member_Alpaca_Data()
    #create the author object
    author = ctx.message.author
    await member.update_keys(str(author.id), live_key, live_secret, paper_key, paper_secret)
    return













#run client on server
client.run('ODY0OTk4MjA3OTI5NzEyNjQw.YO9mWw.7elqzkaRwMOwk57Uouw23SH8qdc')