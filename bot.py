import os 
import json 

import discord 
from dotenv import load_dotenv 

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')


response = 'Hello World!'
ADMIN_PERMISSIONS = 2081422591
client = discord.Client()

def checkAdmin(message): 
    if not message.author.permissions_in(message.channel).administrator: 
        return False 
    
    return True 

@client.event 
async def on_ready(): 
    for guild in client.guilds: 
        if guild.name == GUILD: 
            break 
    
    print( 
        f'{client.user} is connected to the following guild:\n'
        f'{guild.name}(id: {guild.id})'
    )

@client.event
async def on_message(message): 
    if message.author == client.user: 
        return 

    if message.content == '!Hello World': 
        reply = await message.channel.send(response)
        await reply.add_reaction("\N{SLIGHTLY SMILING FACE}")
        await reply.add_reaction("\N{CONFUSED FACE}")
        return 
    
    if '!setgame' in message.content.lower():
        if(message.content == '!setgame'): 
            reply = await message.channel.send('Usage: !setgame [game]')
            return 

        await client.change_presence(activity=discord.Game((message.content).split(' ', 1)[1])) 
        await message.add_reaction('👍')
        return 


    #
    # @discord.on_message 
    # Role Caching for Permissions
    #
    if '!clear' in message.content.lower():

        if not checkAdmin(message):
            await message.channel.send('You do not have permission to use this command!')
            return 
        if (message.content == '!clear'): 
            reply = await message.channel.send('Usage: !clear [size]')
            return 
         
        await message.add_reaction('👍')
        channel = message.channel 

        num = int((message.content).split(' ', 1)[1])

        counter = 0
        async for message in channel.history(limit=num): 
            if(message.author == client.user): 
                counter += 1 
        
        messages = await channel.history(limit=num).flatten() 

        for i in range(len(messages)): 
            tempMessage = messages[i] 
            await tempMessage.delete() 

        await channel.send('Clearing Complete!')




client.run(TOKEN) 