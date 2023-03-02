import os

from discord.ext import commands


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot


    @commands.slash_command(name="listexts", description="List loaded extensions")
    @commands.is_owner()
    async def listexts(self, ctx):
        reply = ["Loaded extensions:"]

        for extension in self.bot.extensions:
            reply.append(f"`{extension}`")
        reply = '\n'.join(reply)

        return await ctx.send_response(content=reply, ephemeral=True)

    @commands.slash_command(name="reloadext", description="Reload extension by name")
    @commands.is_owner()
    async def reloadext(self, ctx, extension: str):
        try:
            self.bot.reload_extension(extension)
            return await ctx.send_response(
                f"Reloaded extension `{extension}`",
                ephemeral=True
            )
        except:
            return await ctx.send_response(
                f"Extension `{extension}` has not been loaded!",
                ephemeral=True
            )

    @commands.slash_command(name="loadext", description="Load an extension")
    @commands.is_owner()
    async def loadext(self, ctx, extension: str):
        try:
            self.bot.load_extension(extension)
            return await ctx.send_response(
                f"Loaded extension `{extension}`",
                ephemeral=True
            )
        except:
            return await ctx.send_response(
                f"An error occurred while trying to load extension `{extension}`",
                ephemeral=True
            )
    

    @commands.slash_command(name="shutdown", description="Shuts down the bot")
    @commands.is_owner()
    async def shutdown(self, ctx):
        await ctx.send_response("Shutting down!", ephemeral=True)
        await self.bot.close()

    @commands.slash_command(name="update", description="Pull from the git repository")
    @commands.is_owner()
    async def update(self, ctx):
        script_dir = os.path.dirname(
            os.path.realpath(__file__)
        )

        os.chdir(script_dir)
        os.chdir('..')

        await ctx.send_response("Updating bot!", ephemeral=True)
        os.system("git pull origin main &> /dev/null")


def setup(bot):
    bot.add_cog(Debug(bot))
