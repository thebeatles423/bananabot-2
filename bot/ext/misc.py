import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
    
    @commands.slash_command(name="vc", description="Send a voice chat link without having to use developer mode")
    async def vc(self, ctx, vc_name: str):
        vc_channel = discord.utils.get(ctx.guild.channels, name=vc_name)
        return await ctx.send_response(vc_channel.mention)


def setup(bot):
    bot.add_cog(Misc(bot))
