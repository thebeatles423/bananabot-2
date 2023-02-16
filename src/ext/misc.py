import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="vc", description="Send a voice chat link without having to use developer mode")
    async def vc(
        self, ctx, 
        vc_name: discord.Option(str, "The name of the vc", required=False, default=None)):
        if vc_name:
            try:
                vc_channel = discord.utils.get(ctx.guild.channels, name=vc_name)
            except:
                return await ctx.send_response("Invalid voice channel!")
            if str(vc_channel.type) == "voice":
                return await ctx.send_response(vc_channel.mention)
            else:
                return await ctx.send_response(f"{vc_channel.mention} is not a voice channel!", ephemeral=True)
        elif ctx.author.voice: # the author is in a vc
            vc_channel = discord.utils.get(ctx.guild.channels, name=vc_name)
            return await ctx.send_response(vc_channel.mention)    
        else:
            return await ctx.send_response("Please specify a voice channel!")


def setup(bot):
    bot.add_cog(Misc(bot))