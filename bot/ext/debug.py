import discord
from discord.ext import commands
from discord import NotFound


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
        try:
            self.bot.reload_extension(extension)
            return await ctx.send_response(content=f"Reloaded extension `{extension}`", ephemeral=True)
        except: # fix this to not be bare except at some point - may cause problems
            return await ctx.send_response(content=f"Extension `{extension}` has not been loaded!", ephemeral=True)
    
    @commands.slash_command(name="send", description="Make the bot send a message.")
    @commands.is_owner()
    async def send(self, ctx, message):
        await ctx.send_response("Message sent!", ephemeral=True)
        return await ctx.send(message)
    
    @commands.message_command(name="Read Message (public)")
    async def read_public(self, ctx, message: discord.Message):
        message = message.content
        message = message.replace('`', r'\`')
        response = "```\n{}\n```".format(message)

        return await ctx.send_response(response)
    
    @commands.message_command(name="Read Message")
    @commands.is_owner()
    async def read(self, ctx, message: discord.Message):
        message = message.content
        message = message.replace('`', r'\`')
        response = "```\n{}\n```".format(message)


def setup(bot):
    bot.add_cog(Debug(bot))