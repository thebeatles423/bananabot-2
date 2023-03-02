import sys

import discord
from discord.ext import commands

# create bot
intents = discord.Intents.all()
bananabot = commands.Bot(command_prefix="b.", intents=intents)


# when the bot starts up
@bananabot.event
async def on_ready():
    print("Bot is connected to discord!")


# when the bot shuts down
def shutdown():
    print("Bot shutting down... ", end="")
    print("done.")

    sys.exit()


# error handling with various other functionality
@bananabot.event
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
@bananabot.event
async def on_application_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send_response("You don't have the permissions to use this command!", ephemeral=True)
    else:
        raise error

extensions = [
    "captionize",
    "debug",
    "define",
    "message",
    "misc",
    #"reminders",
    "rotation",
    "run",
    "search",
    "translate",
    "voice",
]

for extension in extensions:
    bananabot.load_extension(f"ext.{extension}")
