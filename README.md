# DiscordBot
Personal experimentation with python using the discord API 


## Installing and using the bot (linux) 
Clone the repository into a folder 
```
git clone {url} 
```
Install python3 through the cmd prompt using 
```
sudo apt-get install python3 
```
install pip using the get-pip.py method 
```
https://pip.pypa.io/en/stable/installing/
```

Install the discord.py API files using 
```
python3 -m pip install -U discord.py 
```
Followed by the python dotenv libraries 
```
python3 -m pip install -U python_dotenv.py 
```
cd into the cloned repository folder, edit the .env file to include your bots OAuth token and Guild ID (server name) 

Launch the bot using 
```
python3 bot.py 
```

