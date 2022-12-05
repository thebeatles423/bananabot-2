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


# when the bot starts up
@bot.event
async def on_ready():
    print("Bot is connected to discord!")


# error handling
@bot.event
async def on_command_error(ctx, error):
    ignored_errors = (commands.CommandNotFound, commands.UserInputError)
    if isinstance(error, ignored_errors):
        return
    elif isinstance(error, commands.CheckFailure):
        await ctx.reply("You don't have the permissions to use this command!")
        return error


# run code -- see run.py
@bot.command(name="run")
@commands.is_owner()
async def run_code(ctx, *, code_input: str):
    try:
        language = code_input.splitlines()[0].split("```")[1]
    except:
        return await ctx.reply("An unknown error occurred. Did you format the code correctly?")
    
    if language not in run.supported_languages:
        return await ctx.reply("Unsupported language! Did you format the code correctly?")
    else:
        await run.run_code(ctx, language, code_input, global_vars={"ctx": ctx})

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN) # run the bot
