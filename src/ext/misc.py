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

    @commands.is_owner()
    @commands.slash_command() 
    async def af2023(self, ctx: discord.ApplicationContext, nick: str, role: discord.SlashCommandOptionType.role):
        for member in ctx.guild.members:
            try:
                await member.add_roles(role)
                await member.edit(nick=nick)

                ctx.bot.cogs["Autorole"].autoroles.update({member: role})
                ctx.bot.cogs["Autonick"].autonicks.update({member: nick})
            except:
                pass # hehe
        
        await ctx.send_response("Done! (:")
        


def setup(bot):
    bot.add_cog(Misc(bot))