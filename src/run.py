import io
import traceback
from contextlib import redirect_stdout

# list of supported languages, as their respective file extensions
supported_languages: list[str, ...] = ['py']


async def run_code(ctx, language, code_input, global_vars: dict):
        # change stdout
        with io.StringIO() as output, redirect_stdout(output):
            try:
                if code_input.splitlines()[-1] == "```": # if the ending backticks '```' are on a new line
                    code = compile('\n'.join(code_input.splitlines()[1:-1]), "temp", "exec")
                elif code_input[-3:] == "```":
                    code_input = code_input[:-3]
                    code = compile('\n'.join(code_input.splitlines()[1:]), "temp", "exec")
                else:
                    return await ctx.reply("An unknown error occurred. Did you format the code correctly?")
                # execute the compiled code
                exec(code, global_vars)
            except:
                # send error to stdout
                print(traceback.format_exc())
            finally:
                output = output.getvalue()
        
        # if the output has a ` character, it needs to be escaped
        for char, char_index in enumerate(output):
            if char == '`':
                output = output[:char_index] + '\\' + output[char_index:]
        
        if output:
            return await ctx.reply(f"```{output}```")
        else: # if there is no output to stdout
            return await ctx.reply("Your code returned nothing to stdout.")