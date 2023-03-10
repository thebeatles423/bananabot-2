import discord
from discord.ext import commands


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.autodeletes = []
    
    autodelete = discord.SlashCommandGroup("autodelete")
    
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
    @autodelete.command()
    async def add(self, ctx, user: discord.Member):
        if user in self.autodeletes:
            await self.ctx.send_response(
                f"{user.mention} is already in autodeletes!",
                ephemeral=True
            )
        else:
            self.autodeletes.append(user)

            await ctx.send_response(
                f"Added {user.mention} to autodeletes!",
                ephemeral=True
            )
    
    @commands.is_owner()
    @autodelete.command()
    async def remove(self, ctx, user: discord.Member):
        if user not in self.autodeletes:
            await self.ctx.send_response(
                f"{user.mention} is not in autodeletes!",
                ephemeral=True
            )
        else:
            self.autodeletes.remove(user)

            await ctx.send_response(
                f"Removed {user.mention} from autodeletes!",
                ephemeral=True
            )

    @commands.is_owner()
    @autodelete.command()
    async def list(self, ctx):
        if not self.autodeletes:
            await ctx.send_response(
                "There are no users in autodelete!",
                ephemeral=True
            )
        else:
            response = "Users in autodelete:\n"

            for user in self.autodeletes:
                response += user.mention + '\n'

            await ctx.send_response(response, ephemeral=True)

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author in self.autodeletes:
            await message.delete()


def setup(bot):
    bot.add_cog(Misc(bot))