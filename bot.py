import os 
import time 
import sys 
import datetime 

import discord 
from dotenv import load_dotenv 

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
GUILD = os.getenv('DISCORD_GUILD')
currDir = os.getcwd() 
confDir = currDir + '/config'


setgame_usage = 'Usage: !setgame {game}'
clear_usage = 'Usage: !clear {size}'
permission_fail = 'You do not have permission to use this command!'
hello_response = 'Hello World!'
update_message = "I'll be back shortly after an update" 
status_usage = 'Usage: !status {online/idle/dnd/offline} opt:{game}'


client = discord.Client()

def checkAdmin(message): 
    if not message.author.permissions_in(message.channel).administrator: 
        return False 
    
    return True 


def printTime(SERVER, channel, author, raw_message, guild): 
    
    print( datetime.datetime.now().strftime("[%Y-%m-%d @ %H:%M:%S]"), end=' ')
    print( '[' + SERVER + '] '+ '['+guild.name+'] '+ '[#'+ channel.name + '] ' + author.name + ': ' + raw_message)   

    return 


@client.event 
async def on_ready(): 
    
    #os.environ[TEMP] = "1"
    #print ( f'Current working directory: ' + currDir + '\n' ) 
    #print ( f'Config directory: ' + confDir + '\n' )

    #filepath = confDir + '/test.txt'
    #lines = {} 
    #with open(filepath, 'r') as file: 
        #contents = file.readlines() 

    #print(contents)

    #contents[0][0] = 'a' 

    #with open(filepath, 'w') as file: 
        #file.writelines(contents) 

    #print(contents)
    

    print( f'{client.user} is connected to the following guild:\n' )
    for guild in client.guilds: 
        if guild.name: 
            print( f'{guild.name}(id: {guild.id})' )

@client.event
async def on_message(message): 

    author = message.author 
    channel = message.channel 
    raw_message = message.content
    guild = message.guild  
    #mentions = message.mentions    #unused for now
    #guild = message.guild          #unused for now
    SERVER = "DISCORD"  

    if author == client.user: 
        SERVER = "SELFBOT"
        printTime(SERVER, channel, author, raw_message, guild) 
        return 
    
    printTime(SERVER, channel, author, raw_message, guild)

    #
    # Command : !Hello
    # Description : verifies bot can respond in channels 
    #

    if raw_message.lower() == '!hello': 
        reply = await channel.send(hello_response)
        await reply.add_reaction("\N{SLIGHTLY SMILING FACE}")
        print('\t - Added Reaction')
        return 
    

    # 
    # Command : !setgame 
    # Description: sets the current game of the bot 
    #

    if '!setgame' in raw_message.lower():

        if not checkAdmin(message):     #Check if the user has administrator priveledges
            await channel.send(permission_fail)
            return

        if(raw_message == '!setgame'): 
            reply = await channel.send(setgame_usage)
            return 

        await client.change_presence(activity=discord.Game((raw_message).split(' ', 1)[1])) 
        await message.add_reaction('👍')
        print('\t - Set current game to ' + (raw_message).split(' ', 1)[1])
        print('\t - Added Reaction')
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
        print('\t - Added Reaction')
        num = int((raw_message).split(' ', 1)[1]) #Convert {int} to an int 

        counter = 0
        async for message in channel.history(limit=num): #Gather num messages 
            if message.author == client.user: 
                counter += 1 
        
        messages = await channel.history(limit=num).flatten() #Flatten them into a list 

        for i in range(len(messages)):  #Clear them 
            tempMessage = messages[i] 
            await tempMessage.delete(delay=1) 

        print('\t - Cleared ' + str(num) + ' messages')

    #
    # Command : !update
    # Description : restarts the client and clears the console 
    #
    if '!update' in raw_message.lower(): 
        await channel.send(update_message)
        clear = lambda: os.system('clear') 
        clear() 

        for i in range(0, 5):
            b = "Updating" + "." * i
            print(b, end='\r')
            time.sleep(1) 

        os.execv(sys.executable, ['python3'] + sys.argv) 


    def online(): 
        return discord.Status.online 
    def idle(): 
        return discord.Status.idle 
    def dnd(): 
        return discord.Status.dnd
    def offline(): 
        return discord.Status.offline
    
    options = { 
            'online' : online, 
            'idle' : idle, 
            'dnd' : dnd, 
            'offline' : offline, 
    }

    if '!status' in raw_message.lower(): 
        if raw_message.lower() == '!status': 
            await channel.send(status_usage)
            return 

        action = raw_message.split(' ', 2)[1] 

        try: 
            try: 
                subaction = raw_message.split(' ', 2)[2]
                game = discord.Game(subaction) 
                await client.change_presence(status = options[action](), activity = game)  
            except: 
                await client.change_presence(status = options[action]())

            await message.add_reaction('👍') #Confirm command acceptance 
            print('\t - Updated Status to: ' + action)
        except: 
            print('\t - Error: Unknown status')
            await channel.send('Unknown status: ' + action)

        return 


    if raw_message.lower() == '!commands': 
        filepath = confDir + '/commandList.txt'
        with open(filepath, 'r') as file: 
            contents = file.readlines()

        newMsg = ''
        for i in range(len(contents)): 
            contents[i] = contents[i].strip('\n')
            newMsg += contents[i]
            if i != (len(contents)-1): 
                newMsg += ', '

        await channel.send('<@{author}> {msg}'.format(author=author.id, msg=newMsg)) 
        return 

client.run(TOKEN) 
