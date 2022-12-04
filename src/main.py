import logging
import os
import traceback
import sys
import discord
from discord.ext import commands
from dotenv import load_dotenv
from io import StringIO


# load env file for bot token
load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

# create bot
intents = discord.Intents.all()
bot = commands.Bot(command_prefix="b.", intents=intents)

# supported code types for b.run
code_types = ['py']

@bot.command(name="run", description="Execute code in supported languages. This is dangerous, so only special people get to use it (:")
async def run(ctx, *, code_input):
    if ctx.author.id == 934131423059804221:
        try:
            code_type = code_input.splitlines()[0].split('```')[1]
        except Exception as e:
            return await ctx.reply(f"An unknown error occurred: '{e}'")

        if code_type not in code_types:
            return await ctx.reply("Unsupported language! (Or you didn't format the code correctly")
        elif code_type == 'py':
            try:
                code = compile('\n'.join(code_input.splitlines()[1:-1]), "temp", "exec") # assumes the ending backticks are on a new line
                # change stdout 
                old_stdout = sys.stdout
                redirected_output = sys.stdout = StringIO()

                exec(code) # execute the compiled code
                await ctx.reply(f"```{redirected_output.getvalue()}```")

                # change stdout back to normal
                sys.stdout = old_stdout
            except Exception as e:
                return await ctx.reply(e)
    else:
        return await ctx.reply("You don't have the permissions to use this command!")

if __name__ == "__main__":
    bot.run(DISCORD_TOKEN) # run the bot
