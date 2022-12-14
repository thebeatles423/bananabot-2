import asyncio
import io
import time
import traceback
from contextlib import redirect_stdout

import discord
from discord.ext import commands

# list of supported languages, as their respective file extensions
supported_languages: list[str, ...] = ['py']


@commands.command(name="run")
@commands.is_owner()
async def run_code(ctx, *, code_input: str):
    try:
        language = code_input.splitlines()[0].split("```")[1]
    except:
        return await ctx.reply("An unknown error occurred. Did you format the code correctly?")
    
    if language not in supported_languages:
        return await ctx.reply("Unsupported language! Did you format the code correctly?")
    else:
        print("hi")
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, run_in_background, ctx, code_input, language)
        await ctx.reply(result)


def run_in_background(ctx, code_input: str, language: str):
    if language == 'py':
        # change stdout
        with io.StringIO() as output, redirect_stdout(output):
            start = time.perf_counter()
            try:
                if code_input.splitlines()[-1] == "```": # if the ending backticks '```' are on a new line
                    code = compile('\n'.join(code_input.splitlines()[1:-1]), "temp", "exec")
                elif code_input[-3:] == "```":
                    code_input = code_input[:-3]
                    code = compile('\n'.join(code_input.splitlines()[1:]), "temp", "exec")
                else:
                    return "An unknown error occurred. Did you format the code correctly?"
                # execute the compiled code
                exec(code, {'ctx': ctx})
            except:
                # send error to stdout
                print(traceback.format_exc())
            finally:
                finish = time.perf_counter()
                output = output.getvalue()
        
        # if the output has a ` character, it needs to be escaped
        for char, char_index in enumerate(output):
            if char == '`':
                output = output[:char_index] + '\\' + output[char_index:]
        total_time = round((finish - start), 3)
        if output:
            return f"Job finished in {total_time} seconds. ```{output}```"
        else: # if there is no output to stdout
            return f"Job finished in {total_time} seconds. Your code returned nothing to stdout."


def setup(bot):
    bot.add_command(run_code)