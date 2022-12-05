import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

import run

# load env file for bot token
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# create bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="b.", intents=intents)


# run code -- see run.py
@bot.command(name="run")
@commands.is_owner()
async def run_code(ctx, *, code_input: str):
    try:
        language = code_input.splitlines()[0].split("```")[1]
    except:
        return await ctx.reply(f"`An unknown error occurred.\nDid you format the code correctly?`")
    
    if language not in run.supported_languages:
        return await ctx.reply("`Unsupported language!`")
    else:
        await run.run_code(ctx, language, code_input, global_vars={"ctx": ctx})

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN) # run the bot
