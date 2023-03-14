import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.slash_command(name="vc", description="Send a voice chat link without having to use developer mode")
    async def vc(
        self, ctx, 
        vc: discord.Option(
            discord.VoiceChannel,
            required=False
        )
    ):
        if vc:
            return await ctx.send_response(vc.mention)
        elif not vc and (voice := ctx.author.voice):
            return await ctx.send_response(voice.channel.mention)
        else:
            return await ctx.send_response(
                "You're not in a voice channel!",
                ephemeral=True
            )


def setup(bot):
    bot.add_cog(Misc(bot))