import logging
import os

import discord
from dotenv import load_dotenv

# load env file for bot token
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# create client
intents = discord.Intents.default()
client = discord.Client(intents=intents)

# logging setup
handler = logging.FileHandler(filename="discord.log", encoding="utf-8", mode="w")

@client.event
async def on_ready():
    pass


# run the bot
client.run(token=DISCORD_TOKEN,
           log_handler=handler, # write logs out to log file instead of stderr
           log_level=logging.INFO)
