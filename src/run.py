import io
import traceback
from contextlib import redirect_stdout

# list of supported languages, as their respective file extensions
supported_languages: list[str, ...] = ['py']


async def run_code(ctx, language, code_input, global_vars: dict):
        # change stdout
        with io.StringIO() as output, redirect_stdout(output):
            try:
                # assumes the ending backticks '```' are on a new line
                code = compile('\n'.join(code_input.splitlines()[1:-1]), "temp", "exec")
                # execute the compiled code
                exec(code, global_vars)
            except:
                # send error to stdout
                print(f"```{traceback.format_exc()}```") 
            
            output = output.getvalue()
        return await ctx.reply(f"```{output}```")