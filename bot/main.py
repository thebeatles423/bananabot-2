import pickle
import os
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv

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


# when the bot shuts down
def shutdown():
    print("Bot shutting down... ", end="")
    print("done.")

    sys.exit()


# error handling with various other functionality
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.reply("Invalid command.")
        return error
    elif isinstance(error, commands.CheckFailure):
        await ctx.reply("You don't have the permissions to use this command!")
        return error
    else:
        raise error

# separate error handling for application commands
@bot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send_response("You don't have the permissions to use this command!", ephemeral=True)
    else:
        raise error

if __name__ == "__main__":
    # load extensions
    bot.load_extension('ext.run')
    bot.load_extension('ext.debug')
    bot.load_extension('ext.misc')
    bot.load_extension('ext.recording')
    bot.load_extension('ext.reminders')

    try:
        bot.run(token=DISCORD_TOKEN)
    except KeyboardInterrupt:
        shutdown()