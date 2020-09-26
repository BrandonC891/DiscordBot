import os 
import json 

import discord 
from dotenv import load_dotenv 

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')

setgame_usage = 'Usage: !setgame {game}'
clear_usage = 'Usage: !clear {size}'
permission_fail = 'You do not have permission to use this command!'
hello_response = 'Hello World!'


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
    author = message.author 
    channel = message.channel 
    raw_message = message.content 
    #mentions = message.mentions
    guild = message.guild 


    if author == client.user: 
        return 

    #
    # Command : !Hello
    # Description : verifies bot can respond in channels 
    #

    if raw_message.lower() == '!hello': 
        reply = await channel.send(hello_response)
        await reply.add_reaction("\N{SLIGHTLY SMILING FACE}")
        return 
    

    # 
    # Command : !setgame 
    # Description: sets the current game of the bot 
    #

    if '!setgame' in raw_message.lower():
        if(raw_message == '!setgame'): 
            reply = await channel.send(setgame_usage)
            return 

        await client.change_presence(activity=discord.Game((raw_message).split(' ', 1)[1])) 
        await message.add_reaction('👍')
        return 
    
    #
    # Command : !clear {int}
    # Description : clears last {int} number of messages in a channel 
    #

    if '!clear' in raw_message.lower():

        if not checkAdmin(message):     #Check if the user has administrator priveledges
            await channel.send(permission_fail)
            return 

        if raw_message.lower() == '!clear': #Verify proper usage 
            reply = await channel.send(clear_usage)
            return 
         
        await message.add_reaction('👍') #Confirm command acceptance 

        num = int((raw_message).split(' ', 1)[1]) #Convert {int} to an int 

        counter = 0
        async for message in channel.history(limit=num): #Gather num messages 
            if message.author == client.user: 
                counter += 1 
        
        messages = await channel.history(limit=num).flatten() #Flatten them 

        for i in range(len(messages)):  #Clear them 
            tempMessage = messages[i] 
            await tempMessage.delete() 

        await channel.send('Clearing Complete!')

    #
    # Command : !Guild
    # Description : this is a test command
    #
    if '!guild' in raw_message.lower(): 
        #await channel.send(command) 
        await channel.send(guild) 

        guild.Permissions.update()


client.run(TOKEN) 
