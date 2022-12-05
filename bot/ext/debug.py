from discord.ext import commands


class Debug(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.slash_command(name="listexts", description="List loaded extensions.")
    @commands.is_owner()
    async def listexts(self, ctx):
        reply = ["Loaded extensions:"]
        for extension in self.bot.extensions:
            reply.append(f"`{extension}`")
        reply = '\n'.join(reply)

        return await ctx.send_response(content=reply, ephemeral=True)


    @commands.slash_command(name="reloadext", description="Reload extension by name.")
    @commands.is_owner()
    async def reloadext(self, ctx, extension: str):
        self.bot.reload_extension(extension)
        return await ctx.send_response(content=f"Reloaded extension `{extension}`", ephemeral=True)


def setup(bot):
    bot.add_cog(Debug(bot))