from discord.ext.commands.core import command
from discord.ext import commands
import discord
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

@client.command(name='account')
async def account(ctx):
    '''This functions gets the alpaca account. the parameters mirror the ones from our alpaca module'''
    
    #create instance of member_alpaca_data class and read in the dataframe
    member = Member_Alpaca_Data()
    await member.read_csv()
    #create the author object
    author = ctx.message.author
    #create the broker object
    broker = Alpaca_Account(member.user_dictionary[str(author.id)]['Live_Key'],member.user_dictionary[str(author.id)]['Live_Secret'],member.user_dictionary[str(author.id)]['Paper_Key'],member.user_dictionary[str(author.id)]['Paper_Secret'])
    if ctx.channel.id == 863095775407505478:
        await broker.get_account(live=True)
    elif ctx.channel.id == 863095208819294278:
        await broker.get_account(live=False)
    
    #create the embed
    broker_embed = discord.Embed(title=f'Bitllionaire Broker', description='Brokerage Account', color=0x00ff00)
    for key in broker.response_dict:
        broker_embed.add_field(name=key, value=f'{broker.response_dict[key]}\n', inline=False)
    
    #add footer and thumbnail
    broker_embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/792763798645637130/849786769687314482/imgbin_bitcoin-cash-cryptocurrency-bitcoin-gold-ethereum-png.png')
    broker_embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/792763798645637130/849786769687314482/imgbin_bitcoin-cash-cryptocurrency-bitcoin-gold-ethereum-png.png', 
    text="The Bitllionaire's Club. Formula-X LLC")
    
    #send the embed
    await ctx.message.author.send(embed=broker_embed)

@client.command(name='quote')
async def quote(ctx, symbol):
    '''This functions gets the alpaca account. the parameters mirror the ones from our alpaca module'''
    
    #create instance of member_alpaca_data class and read in the dataframe
    member = Member_Alpaca_Data()
    await member.read_csv()
    #create the author object
    author = ctx.message.author
    #create the broker object
    broker = Alpaca_Account(member.user_dictionary[str(author.id)]['Live_Key'],member.user_dictionary[str(author.id)]['Live_Secret'],member.user_dictionary[str(author.id)]['Paper_Key'],member.user_dictionary[str(author.id)]['Paper_Secret'])
    #route to the correct channel
    if ctx.channel.id == 863095775407505478:
        await broker.get_quote(symbol=symbol)
    elif ctx.channel.id == 863095208819294278:
        await broker.get_quote(symbol=symbol)
    
    #create the embed
    broker_embed = discord.Embed(title=f'Bitllionaire Broker', description='Brokerage Account', color=0x00ff00)
    for key in broker.response_dict:
        broker_embed.add_field(name=key, value=f'{broker.response_dict[key]}\n', inline=False)
        break
    for key in broker.response_dict.get('quote'):
        broker_embed.add_field(name=key, value=f'{broker.response_dict.get("quote")[key]}\n', inline=False)
    
    #add footer and thumbnail
    broker_embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/792763798645637130/849786769687314482/imgbin_bitcoin-cash-cryptocurrency-bitcoin-gold-ethereum-png.png')
    broker_embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/792763798645637130/849786769687314482/imgbin_bitcoin-cash-cryptocurrency-bitcoin-gold-ethereum-png.png', 
    text="The Bitllionaire's Club. Formula-X LLC")
    
    #send the embed
    await ctx.message.channel.send(embed=broker_embed)

@client.command(name='positions')
async def positions(ctx):
    '''This functions gets the alpaca account. the parameters mirror the ones from our alpaca module'''
    
    #create instance of member_alpaca_data class and read in the dataframe
    member = Member_Alpaca_Data()
    await member.read_csv()
    #create the author object
    author = ctx.message.author
    #create the broker object
    broker = Alpaca_Account(member.user_dictionary[str(author.id)]['Live_Key'],member.user_dictionary[str(author.id)]['Live_Secret'],member.user_dictionary[str(author.id)]['Paper_Key'],member.user_dictionary[str(author.id)]['Paper_Secret'])
    if ctx.channel.id == 863095775407505478:
        await broker.get_all_positions(live=True)
    elif ctx.channel.id == 863095208819294278:
        await broker.get_all_positions(live=False)
    
    #create a for loop that parses the response and creates the embed
    for item in broker.response_dict:
        broker_embed = discord.Embed(title=f'Bitllionaire Broker', description='Brokerage Account', color=0x00ff00)
        for key in item:
            broker_embed.add_field(name=key, value=f'{item[key]}\n', inline=False)
 
        #add footer and thumbnail
        broker_embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/792763798645637130/849786769687314482/imgbin_bitcoin-cash-cryptocurrency-bitcoin-gold-ethereum-png.png')
        broker_embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/792763798645637130/849786769687314482/imgbin_bitcoin-cash-cryptocurrency-bitcoin-gold-ethereum-png.png', 
        text="The Bitllionaire's Club. Formula-X LLC")
        
        #send the embed
        await ctx.message.author.send(embed=broker_embed)
        # break

@client.command(name='position')
async def position(ctx, symbol):
    '''This functions gets the alpaca account. the parameters mirror the ones from our alpaca module'''
    
    #create instance of member_alpaca_data class and read in the dataframe
    member = Member_Alpaca_Data()
    await member.read_csv()
    #create the author object
    author = ctx.message.author
    #create the broker object
    broker = Alpaca_Account(member.user_dictionary[str(author.id)]['Live_Key'],member.user_dictionary[str(author.id)]['Live_Secret'],member.user_dictionary[str(author.id)]['Paper_Key'],member.user_dictionary[str(author.id)]['Paper_Secret'])
    #route to the correct channel
    if ctx.channel.id == 863095775407505478:
        await broker.get_position(symbol=symbol, live=True)
    elif ctx.channel.id == 863095208819294278:
        await broker.get_position(symbol=symbol, live=False)
    
    #create the embed
    broker_embed = discord.Embed(title=f'Bitllionaire Broker', description='Brokerage Account', color=0x00ff00)
    for key in broker.response_dict:
        broker_embed.add_field(name=key, value=f'{broker.response_dict[key]}\n', inline=False)
    
    #add footer and thumbnail
    broker_embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/792763798645637130/849786769687314482/imgbin_bitcoin-cash-cryptocurrency-bitcoin-gold-ethereum-png.png')
    broker_embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/792763798645637130/849786769687314482/imgbin_bitcoin-cash-cryptocurrency-bitcoin-gold-ethereum-png.png', 
    text="The Bitllionaire's Club. Formula-X LLC")

    #send the embed
    await ctx.message.channel.send(embed=broker_embed)

@client.command(name='orders')
async def orders(ctx, status='open'):
    '''This functions gets the alpaca account. the parameters mirror the ones from our alpaca module'''
    
    #create instance of member_alpaca_data class and read in the dataframe
    member = Member_Alpaca_Data()
    await member.read_csv()
    #create the author object
    author = ctx.message.author
    #create the broker object
    broker = Alpaca_Account(member.user_dictionary[str(author.id)]['Live_Key'],member.user_dictionary[str(author.id)]['Live_Secret'],member.user_dictionary[str(author.id)]['Paper_Key'],member.user_dictionary[str(author.id)]['Paper_Secret'])
    if ctx.channel.id == 863095775407505478:
        await broker.get_orders(status=status, live=True)
    elif ctx.channel.id == 863095208819294278:
        await broker.get_orders(status=status, live=False)
    
    #create a for loop that parses the response and creates the embed
    for item in broker.order_response:
        broker_embed = discord.Embed(title=f'Bitllionaire Broker', description='Brokerage Account', color=0x00ff00)
        for key in item: #Loop through each key in the dict
            if item[key]: #if the key and value exist add it to the field to avoid errors
                broker_embed.add_field(name=key, value=f'{item[key]}\n', inline=False)
 
        #add footer and thumbnail
        broker_embed.set_thumbnail(url='https://cdn.discordapp.com/attachments/792763798645637130/849786769687314482/imgbin_bitcoin-cash-cryptocurrency-bitcoin-gold-ethereum-png.png')
        broker_embed.set_footer(icon_url='https://cdn.discordapp.com/attachments/792763798645637130/849786769687314482/imgbin_bitcoin-cash-cryptocurrency-bitcoin-gold-ethereum-png.png', 
        text="The Bitllionaire's Club. Formula-X LLC")
        
        #send the embed
        await ctx.message.author.send(embed=broker_embed)
        # break
        


#run client on server
client.run('ODY0OTk4MjA3OTI5NzEyNjQw.YO9mWw.7elqzkaRwMOwk57Uouw23SH8qdc')