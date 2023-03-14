import discord
from discord.ext import commands


class Autodelete(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.autodeletes = []
    
    autodelete = discord.SlashCommandGroup("autodelete")
    
    @commands.is_owner()
    @autodelete.command()
    async def add(self, ctx, user: discord.Member):
        if user in self.autodeletes:
            await ctx.send_response(
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
            await ctx.send_response(
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


class Autonick(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        
        self.autonicks = {}
    
    autonick = discord.SlashCommandGroup("autonick")
    
    @commands.is_owner()
    @autonick.command()
    async def add(self, ctx, user: discord.Member, nick: str):
        if user in self.autonicks:
            await ctx.send_response(
                f"{user.mention} is already in autonicks!",
                ephemeral=True
            )
        elif user in self.autonicks and nick != self.autonicks[user]:
            self.autonicks[user] = nick
            await user.edit(nick=nick)
        elif user in self.autonicks and nick == self.autonicks[user]:
            await ctx.send_response(
                f"{user.mention} already has the nick {nick}!",
                ephemeral=True
            )
        else:
            try:
                await user.edit(nick=nick)
            except:
                return await ctx.send_response(
                    f"I can't nickname {user.mention}!",
                    ephemeral=True
                )
            self.autonicks.update({user: nick})

            await ctx.send_response(
                f"Added {user.mention} to autonicks!",
                ephemeral=True
            )
    
    @commands.is_owner()
    @autonick.command()
    async def remove(self, ctx, user: discord.Member):
        if user not in self.autonicks:
            await ctx.send_response(
                f"{user.mention} is not in autonicks!",
                ephemeral=True
            )
        else:
            del self.autonicks[user]

            await ctx.send_response(
                f"Removed {user.mention} from autonicks!",
                ephemeral=True
            )

    @commands.is_owner()
    @autonick.command()
    async def list(self, ctx):
        if not self.autonicks:
            await ctx.send_response(
                "There are no users in autonick!",
                ephemeral=True
            )
        else:
            response = "Users in autonick:\n"

            for user in self.autonicks:
                response += f"{user.mention}: {self.autonicks[user]}\n"

            await ctx.send_response(response, ephemeral=True)

    @commands.Cog.listener()
    async def on_member_update(self, before: discord.Member, after: discord.Member):
        if before in self.autonicks or after in self.autonicks:
            await after.edit(nick=self.autonicks[after])


def setup(bot):
    bot.add_cog(Autodelete(bot))
    bot.add_cog(Autonick(bot))